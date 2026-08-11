---
title: "Week 10 Flipped Material"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Week 10 Flipped Material

**Complete this before Week 11's class.** Week 11 is a big day: a live PXE demo on real hardware, Lab9, Quiz9, and Test 3 all happen that session. This reading gets you the concepts behind the demo — you won't need to set anything up yourself before class.

## How Network Booting Works: DHCP, TFTP, and the PXE Chain

Every machine you've provisioned this term already had an operating system installed before Terraform, Packer, or Cloud-Init ever touched it — AWS handed you a running instance from an existing image. Week 11 goes one layer deeper: installing an OS onto a machine that has **nothing** on its disk yet, using only the network.

This is what PXE (Preboot eXecution Environment) does. At a conceptual level, four things have to happen in order:

1. **DHCP discovery.** The target machine's firmware broadcasts a request for an IP address, the same way any device joining a network does. A normal DHCP server can answer this — but a PXE boot also needs two extra pieces of information a typical home/office router doesn't provide: which server to fetch a bootloader from, and what that bootloader's filename is.

2. **TFTP: fetching the bootloader and kernel.** TFTP (Trivial File Transfer Protocol) is a stripped-down, no-authentication file transfer protocol — intentionally simple, because it has to run inside firmware before any real operating system exists. The target machine uses TFTP to pull down a small bootloader, which in turn pulls down a slightly larger boot manager, which finally pulls down the actual Linux kernel and initial ramdisk (initrd).

3. **The kernel takes over.** Once the kernel and initrd are loaded into memory and execution jumps to them, the machine is running Linux — just not yet installed anywhere. From here it needs the actual installer program and OS files.

4. **HTTP: fetching the installer payload.** TFTP is too slow and limited for transferring a multi-gigabyte OS image, so once the kernel is running, it switches to a full HTTP request to fetch the installer and the OS files themselves — and, if the installation is unattended, a configuration file describing exactly how to partition the disk, set the hostname, and create the initial user account.

**Read:** skim the [Ubuntu Server autoinstall documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/) introduction/overview page to see what an unattended install configuration actually specifies — you don't need to memorize the syntax, just recognize the shape of it.

Come to Week 11 ready to answer: why does this whole process need three different protocols (DHCP, TFTP, HTTP) instead of just one?

---
*Reminder: Quiz9, Lab9, and Test 3 all happen in Week 11. Quiz9 draws on this reading and today's Week 10 lecture (Ansible loops, conditionals, handlers, and roles).*
{% endraw %}
