# Lab 1: Local Development Environment Setup

This lab sets up the local development environment you'll use for the rest of the course. Nearly every tool from here on (Terraform, Packer, Ansible) has limited or no native Windows/macOS support, so a working Linux environment is the foundation everything else builds on.

## Prerequisites
- A computer with virtualization enabled in the BIOS/UEFI.
- Administrative (root) privileges on your machine.

---

## 1. Operating System Environment

You need a **Debian Linux environment** — specifically Debian 13 ("trixie") or Debian 14 ("forky"), or Ubuntu 22.04+ (Ubuntu is Debian-based and works for everything in this course).

Choose **one** of the following, depending on your host OS:

### Option A: Windows Subsystem for Linux (WSL2)
*Recommended path for Windows 10/11.*
1. Open an administrative PowerShell prompt.
2. Run `wsl --install -d Debian` (or `wsl --install` for the default Ubuntu, which also works).
3. Create your default UNIX user and password when prompted.
4. **Enable `systemd` support.** From your WSL terminal, edit `/etc/wsl.conf`:
   ```ini
   [boot]
   systemd=true
   ```
5. Restart WSL completely — `wsl --shutdown` from PowerShell, then reopen your Linux app.
6. **Work from the Linux filesystem, not the Windows one.** If your prompt starts with `/mnt/c/Users/...`, you're on the Windows filesystem — move to your Linux home directory (`~`) instead. This isn't optional: Windows' default file permissions are more permissive than Debian's, and several tools this term (SSH in particular) will fail with confusing permission errors if your files live under `/mnt/c`.
7. If WSL2 setup fails, you may need to enable Hyper-V manually from an elevated PowerShell prompt:
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```

See [WSL-Resources.md](./WSL-Resources.md) for more detail on all of the above, including why working from the Linux filesystem matters for performance, not just permissions.

### Option B: Virtual Machine (VirtualBox or VMware)
*Recommended for macOS (Intel) users, or Windows users who can't use WSL.*
1. Download the [Debian](https://www.debian.org/download) or [Ubuntu 22.04+](https://ubuntu.com/download) Server or Desktop ISO.
2. Create a new VM with at least 2 CPU cores and 4 GB RAM.
3. Complete the standard installation.

---

## 2. Setting Up Your Editor (VS Code)

1. Install [VS Code](https://code.visualstudio.com/) on your host machine (Windows or macOS).
2. **WSL users:** install the `WSL` extension in VS Code.
3. **VM users:** use the `Remote - SSH` extension to connect VS Code on your host to your Linux VM.

**Verify it worked:** from your Linux terminal, run `code .` inside any directory. VS Code should open, connected to that Linux directory.

---

## 3. Version Control (Git)

Every artifact you build this term — Terraform configs, Ansible playbooks, Packer templates — is version-controlled and synced to GitLab.

1. Install Git:
   ```bash
   sudo apt update
   sudo apt install git -y
   ```
2. Configure your identity:
   ```bash
   git config --global user.name "Your Full Name"
   git config --global user.email "your.student.email@bcit.ca"
   ```
3. Set your default branch name:
   ```bash
   git config --global init.defaultBranch main
   ```

---

## 4. Verify systemd Is Working

Since several labs this term depend on managing services with `systemctl`, confirm it's actually functional now rather than discovering it's broken in Week 2:
```bash
systemctl status
```
This should return system status information without an error. If it errors, revisit step 4 under Option A (WSL users) — `systemd=true` most likely isn't set, or WSL wasn't fully restarted afterward.

---

## 5. Container Runtime (Incus)

We'll use this later in the term to compare container, VM, and bare-metal infrastructure directly. Installing it now means any setup issues get caught while you have help in the room.

1. Install Incus:
   ```bash
   sudo apt update
   sudo apt install -y incus
   ```
2. Add yourself to the `incus-admin` group and re-open your terminal (or run `newgrp incus-admin`):
   ```bash
   sudo usermod -aG incus-admin $USER
   ```
3. Initialize with minimal defaults:
   ```bash
   sudo incus admin init --minimal
   ```
4. Launch a test container and confirm it's running:
   ```bash
   incus launch images:debian/13 test-container
   incus list
   ```
5. Confirm systemd is actually working inside the container (not just the shell):
   ```bash
   incus exec test-container -- systemctl status
   ```
6. Clean up — we'll relaunch this fresh in Week 7:
   ```bash
   incus delete test-container --force
   ```

---

## Completion Checklist

Show your instructor or TA that you have:
1. A running Linux (Debian/Ubuntu) terminal, working from the Linux filesystem.
2. `systemctl status` returning without error.
3. VS Code launching successfully from your Linux environment (`code .`).
4. Git installed and configured with your name and BCIT email.
5. Incus installed, test container launched, `systemctl status` confirmed working inside it.
