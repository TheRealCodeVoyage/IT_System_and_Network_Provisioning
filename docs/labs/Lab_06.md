---
title: "Lab 6: Introduction to Ansible"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Lab 6: Introduction to Ansible

Today you'll set up a control node, target one or more managed nodes over SSH, run ad-hoc commands, then write and run your first playbook — checking that it's idempotent along the way.

## Prerequisites
- A control machine (your WSL/Linux environment) with Python 3 installed.
- At least one managed node reachable over SSH (a Lab 3/4 EC2 instance works well — reuse one, or launch a fresh `t2.micro`).
- Passwordless SSH (key-based) already working to the managed node — reuse your `~/.ssh/config` setup from Lab 2.

---

## Part A: Install Ansible and Build an Inventory

Install Ansible on the control node:
```bash
sudo apt update
sudo apt install -y ansible
ansible --version
```

Create a project directory and an inventory file:
```bash
mkdir -p ~/ansible-lab && cd ~/ansible-lab
```

`inventory/hosts.yml`:
```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: <your-EC2-public-IP>
          ansible_user: ubuntu
          ansible_ssh_private_key_file: ~/.ssh/my_aws_key.pem
```

Create `ansible.cfg` in the project root so Ansible finds your inventory without `-i` every time:
```ini
[defaults]
inventory = ./inventory/hosts.yml
host_key_checking = False
```

## Part B: Ad-hoc Commands

Confirm connectivity, then run a few one-off commands directly against the inventory:
```bash
ansible webservers -m ping
ansible webservers -a "uptime"
ansible webservers -m apt -a "name=nginx state=present" --become
```
The `-m` flag picks a module (`ping`, `apt`); without `-m`, Ansible defaults to the `command` module. `--become` runs the task with elevated privileges (sudo) on the managed node.

## Part C: Write a Playbook

`webservers.yml`:
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: true

    - name: Ensure nginx is running and enabled
      service:
        name: nginx
        state: started
        enabled: true

    - name: Deploy custom index page
      copy:
        content: "Configured by Ansible - {{ inventory_hostname }}\n"
        dest: /var/www/html/index.html
```

Check the syntax before running anything:
```bash
ansible-playbook --syntax-check webservers.yml
```

Run it:
```bash
ansible-playbook webservers.yml
```
Visit the managed node's public IP in a browser to confirm the page is live.

## Part D: Verify Idempotence

Run the exact same playbook a second time, with no changes to the target in between:
```bash
ansible-playbook webservers.yml
```
Compare the `PLAY RECAP` from both runs. The first run should show tasks reported as `changed`; the second run should show the same tasks as `ok` with `changed=0`. This is idempotence: running a playbook repeatedly against a system that's already in the desired state produces no further changes. If your second run shows `changed` tasks, something in your playbook isn't idempotent — check whether you used a module (like `copy` or `apt`) correctly rather than a raw `command`/`shell` task, which re-runs unconditionally.

---

## Completion

Show your instructor or TA:
1. `ansible webservers -m ping` succeeding against your managed node.
2. Your `webservers.yml` playbook running successfully (first run, showing `changed` tasks).
3. The same playbook run a second time, showing `changed=0` — proof of idempotence.
4. The custom page live in a browser at the managed node's IP.
{% endraw %}
