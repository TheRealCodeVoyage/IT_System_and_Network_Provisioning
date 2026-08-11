# Week 1 Flipped Material

**Complete this before Week 2's class.** Week 2 opens with a quiz drawing on this material plus a recap of Week 1's lecture, and the in-class lab that day builds directly on these concepts — you'll be behind fast if you skip the reading.

## 1. Bash Variables, Environment Variables & Command Substitution
We'll be writing automation scripts throughout the term. Before we do, you need to be comfortable storing and retrieving variables, exporting environment variables, and capturing a command's output into a variable (command substitution) — this last one is how we'll later grab an AWS resource ID from one command and feed it into the next.
- **Read:** [Bash Variables, Environment Variables, and Command Substitution](https://docs.rockylinux.org/books/learning_bash/02-using-variables/)

## 2. Bash Heredocs
A heredoc lets a script write a multi-line block of text — often a whole config file — without a wall of `echo` statements. We'll use this constantly to generate configuration files dynamically from scripts.
- **Read:** [Understanding the Bash Heredoc](https://linuxize.com/post/bash-heredoc/)

## 3. Linux Service Management (`systemctl`)
Modern Linux distributions manage background services (web servers, databases, and — later this term — the provisioning services you'll run yourself) with `systemd`. You need to be able to start, stop, enable, and check the status of a service before Week 2.
- **Read:** [Introduction to systemctl commands](https://www.linode.com/docs/guides/introduction-to-systemctl/)

## 4. Secure Shell (SSH) Fundamentals
SSH is how you'll reach every remote system this term — AWS instances, GitLab, and later the bare-metal provisioning server. Week 2 has you generating keys and configuring passwordless connections, so read up on what's actually happening during an SSH handshake first.
- **Read:** [What Is SSH: Understanding Encryption, Ports, and Connection](https://www.hostinger.com/tutorials/ssh-tutorial-how-does-ssh-work)

---

*Starting next week, bring a pen or pencil and paper to class for in-class architecture activities.*
