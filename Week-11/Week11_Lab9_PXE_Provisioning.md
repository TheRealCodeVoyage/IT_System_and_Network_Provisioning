# Lab 9: Bare-Metal Provisioning with PXE

Today you'll build a complete network-boot provisioning stack from scratch — entirely inside VirtualBox on your own laptop. You'll run two VMs: one plays the role of a **provisioning server** (DHCP, TFTP, and HTTP, from scratch), the other is a **PXE client** that boots and installs an OS with no installation media at all — just the network.

This is the same chain of protocols (DHCP → TFTP → HTTP) covered in this week's lecture and last week's reading, and the same chain your instructor used to provision real bare-metal hardware — you're building your own miniature version of it.

## Prerequisites
- VirtualBox 7.x installed, with enough free disk space for two small VMs (~15 GB total is plenty).
- An Ubuntu Server 22.04 (or 24.04) ISO downloaded already — you'll need it twice: once to install the provisioning server VM normally, and once to serve as the network-installable OS for the PXE client.
- Comfort with basic Linux service management (`systemctl`) and editing config files — this is a heavier lab than most; budget a full session for it.

---

## Part A: Build the Isolated Network

Before creating either VM, create a private network that only your two VMs will ever see.

1. Open **VirtualBox → Tools → Network Manager** (or **File → Tools → Network Manager**).
2. Under **Internal Networks**, note that these are created automatically the first time a VM's adapter references one — you don't need to pre-create it. You'll name it `pxenet` when configuring each VM's NIC in Part B and Part C.

**Why Internal Network, specifically, and not "Host-only" or "Bridged":**
- **Bridged** would put your PXE traffic on your real WiFi/Ethernet network — this is exactly the setup this course's own hardware testing found unreliable (WiFi chipsets rewriting MAC addresses breaks DHCP in inconsistent, hard-to-debug ways).
- **Host-only** networks come with VirtualBox's *own* built-in DHCP server already running on them, which would fight with the dnsmasq DHCP server you're about to build.
- **Internal Network** is a closed, VirtualBox-only network with nothing else running on it — an empty room where dnsmasq is the only authority. That makes it the simplest and most reliable option for a self-contained PXE lab.

---

## Part B: Build the Provisioning Server VM

### B.1 Create and install the VM

1. Create a new VM named `provisioning-server`: 2 GB RAM, 1 CPU, 15 GB disk, type Linux/Ubuntu (64-bit).
2. Give it **two network adapters**:
   - **Adapter 1:** NAT — this gives the VM internet access so you can install packages. You'll only need this temporarily.
   - **Adapter 2:** Internal Network, named `pxenet` — this is the network your PXE client will boot over.
3. Attach the Ubuntu Server ISO and install normally (interactive install is fine — this VM itself is not being network-installed). Give it hostname `provisioning-server` and a username/password you'll remember.
4. Once installed and booted, confirm both interfaces are up:
   ```bash
   ip a
   ```
   You should see two interfaces beyond `lo` — one with a NAT-assigned address (something like `10.0.2.15`), one with no address yet (the internal network adapter — you'll assign that next).

### B.2 Configure a static IP on the internal-network adapter

Identify which interface is which with `ip a` (match by MAC address shown in VirtualBox's adapter settings if it's not obvious), then set a static address on the internal-network one. Assuming it's `enp0s8`:

`/etc/netplan/01-pxenet.yaml`:
```yaml
network:
  version: 2
  ethernets:
    enp0s8:
      addresses:
        - 192.168.50.1/24
```
Apply it:
```bash
sudo netplan apply
ip a show enp0s8   # confirm 192.168.50.1/24 is assigned
```

### B.3 Install the required packages

```bash
sudo apt update
sudo apt install -y dnsmasq nginx pxelinux syslinux-common
```

### B.4 Lay out the TFTP directory

```bash
sudo mkdir -p /srv/tftp/pxelinux.cfg
sudo cp /usr/lib/PXELINUX/pxelinux.0 /srv/tftp/
sudo cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/
```
> **Common gotcha:** `pxelinux.0` alone isn't enough — it dynamically loads `ldlinux.c32` from the same directory at boot. If you skip copying it, the client will fetch `pxelinux.0` successfully and then silently hang. If your boot stalls right after the bootloader loads, check for this file first.

### B.5 Configure dnsmasq as the DHCP + TFTP server

`/etc/dnsmasq.d/pxe.conf`:
```ini
# Only listen on the internal-network interface — never the NAT adapter
interface=enp0s8
bind-interfaces

# This is a full, authoritative DHCP server — safe here because
# nothing else on this isolated network hands out addresses.
dhcp-range=192.168.50.10,192.168.50.100,12h

# Legacy BIOS PXE boot file (see the note on EFI below)
dhcp-boot=pxelinux.0

enable-tftp
tftp-root=/srv/tftp
```

> **Why no `pxe-service` proxyDHCP lines here, unlike some real-world setups you may read about:** proxyDHCP is only needed when a *second*, separate DHCP server (like a home router) is already handing out addresses and you need to piggyback PXE-specific options on top of it. Here, dnsmasq is the *only* DHCP server on this network, so it can just answer every part of the request directly — simpler by construction.

> **Why legacy BIOS instead of UEFI:** VirtualBox 7.1's UEFI firmware has a known regression that makes EFI+PXE netboot unreliable. Disabling EFI on the client VM (Part C) and using the older PXELINUX chain here avoids that regression entirely. This is a different (but equally valid) boot chain from the UEFI shim/GRUB chain used on real modern hardware — don't be surprised if you read about `bootx64.efi`/`grubx64.efi` elsewhere; that's the UEFI equivalent of what you're building here.

Restart and check:
```bash
sudo systemctl restart dnsmasq
sudo systemctl status dnsmasq   # should show "active (running)"
```

### B.6 Get a kernel, initrd, and installer ISO in place

```bash
cd /tmp
wget https://releases.ubuntu.com/22.04/ubuntu-22.04.4-live-server-amd64.iso
sudo mount ubuntu-22.04.4-live-server-amd64.iso /mnt

sudo cp /mnt/casper/vmlinuz /srv/tftp/
sudo cp /mnt/casper/initrd /srv/tftp/

sudo mkdir -p /var/www/html/ubuntu
sudo cp /tmp/ubuntu-22.04.4-live-server-amd64.iso /var/www/html/ubuntu/

sudo umount /mnt
```

### B.7 Write the PXELINUX boot menu

`/srv/tftp/pxelinux.cfg/default`:
```
DEFAULT install
LABEL install
  KERNEL vmlinuz
  APPEND initrd=initrd ip=dhcp url=http://192.168.50.1/ubuntu/ubuntu-22.04.4-live-server-amd64.iso ---
```

### B.8 Serve the ISO over HTTP

The default nginx site on port 80 already serves `/var/www/html` — confirm it's actually listening there (some systems have another service already bound to port 80):
```bash
sudo ss -tlnp | grep ':80\b'
```
If nginx isn't the process bound to port 80 (for example if you'd previously installed something else), edit `/etc/nginx/sites-enabled/default`'s `listen` directive to an open port instead, and update the `url=` line in Part B.7 to match.

Confirm the ISO is actually reachable:
```bash
curl -I http://192.168.50.1/ubuntu/ubuntu-22.04.4-live-server-amd64.iso
```
You should see `HTTP/1.1 200 OK`. If you get a 404, double-check the file actually landed in `/var/www/html/ubuntu/`.

---

## Part C: Build the PXE Client VM

1. Create a new VM named `pxe-client`: 2 GB RAM, 1 CPU, 15 GB disk, type Linux/Ubuntu (64-bit). **Do not attach an installation ISO** — this VM has to boot from the network, not from local media.
2. **Disable EFI:** Settings → System → Motherboard → uncheck **Enable EFI**. (This is the step that avoids VirtualBox 7.1's UEFI+PXE regression.)
3. **Set boot order:** Settings → System → Motherboard → Boot Order → move **Network** to the top, above Hard Disk and Optical.
4. **Network adapter:** Settings → Network → Adapter 1 → Attached to: **Internal Network**, name: `pxenet` — must exactly match the provisioning server's second adapter.
5. Leave the virtual hard disk attached and empty — the installer will partition it.

---

## Part D: Boot It

1. Make sure `provisioning-server` is running first.
2. Start `pxe-client`.
3. Watch the boot sequence in the VM window. You should see, in order:
   - A DHCP address obtained (briefly visible in the boot log)
   - `pxelinux.0` fetched over TFTP
   - The PXELINUX menu appearing (it will auto-select `install` after a short timeout)
   - The kernel and initrd loading
   - The Ubuntu installer starting, and — since it's fetching over HTTP — a short pause while it downloads the ISO contents

**Minimum success checkpoint:** reaching the Subiquity installer's language/welcome screen confirms your entire DHCP → TFTP → HTTP chain worked end-to-end. That's the deliverable for this lab.

**Optional stretch goal:** continue through the interactive installer to a completed install and first boot.

---

## Part E: Diagnostics (use if something doesn't boot)

```bash
# Watch DHCP/TFTP traffic live, on the provisioning server, before powering on the client
sudo systemctl stop dnsmasq
sudo dnsmasq --no-daemon -d --log-dhcp --conf-file=/etc/dnsmasq.d/pxe.conf
```
Power on `pxe-client` in a second window and watch the log. You're looking for, in order: a `DHCPDISCOVER` from the client's MAC, a `DHCPOFFER` back, then a TFTP request for `pxelinux.0`.

| Symptom | Likely cause | Check |
|---|---|---|
| Client never gets an IP | Adapter names don't match, or dnsmasq isn't listening on the right interface | Confirm both VMs' internal-network adapter names are exactly `pxenet`; confirm `interface=` in `pxe.conf` matches `ip a` on the server |
| DHCP works, but nothing loads after | `pxelinux.0` or `ldlinux.c32` missing from `/srv/tftp/` | Re-check Part B.4 |
| Bootloader loads, then hangs | Usually the missing `ldlinux.c32` gotcha from B.4 | Confirm the file exists and is readable |
| Installer starts, then fails to fetch the ISO | HTTP server not reachable at the `url=` address/port in `pxelinux.cfg/default` | `curl -I` the exact URL from another terminal on the server itself |
| Client boots straight to an empty disk / "no bootable device" instead of PXE | Boot order not actually set to Network first, or EFI still enabled | Re-check Part C steps 2 and 3 |

---

## Completion

Show your instructor or TA:
1. `provisioning-server`'s dnsmasq and nginx both `active (running)`, with `/srv/tftp/` and `/var/www/html/ubuntu/` populated as described.
2. `pxe-client` booting via PXE and reaching the Ubuntu installer's welcome screen (minimum), or a completed install (stretch goal).
3. A brief walkthrough, in your own words, of what each of the three protocols (DHCP, TFTP, HTTP) did during that boot.
