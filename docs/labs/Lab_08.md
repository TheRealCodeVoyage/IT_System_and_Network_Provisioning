---
title: "Lab 8: Ansible Loops, Conditionals, Handlers & Roles"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Lab 8: Ansible Loops, Conditionals, Handlers & Roles

Today you'll extend Lab 6's `webservers.yml` playbook with a loop, a conditional, and a handler — then refactor the whole thing into a reusable role.

## Prerequisites
- Lab 6 completed, with a working `ansible-lab/` project and inventory.
- Your managed node from Lab 6 (or a fresh EC2 instance) still reachable over SSH.

---

## Part A: Add a Loop

Add a task to `webservers.yml` that creates several users at once, using a loop over a list of hashes:

```yaml
- name: Create application users
  ansible.builtin.user:
    name: "{{ item.name }}"
    state: present
    groups: "{{ item.groups }}"
  loop:
    - { name: 'deploy', groups: 'sudo' }
    - { name: 'monitor', groups: 'adm' }
```

Run it:
```bash
ansible-playbook webservers.yml
```
Confirm both users exist on the managed node:
```bash
ansible webservers -a "getent passwd deploy monitor"
```

---

## Part B: Add a Conditional

Add a task that only runs based on a gathered fact — the OS family:

```yaml
- name: Report OS family
  ansible.builtin.debug:
    msg: "This host is running {{ ansible_facts['os_family'] }}"

- name: Install a package only on Debian-family hosts
  ansible.builtin.apt:
    name: tree
    state: present
  when: ansible_facts['os_family'] == "Debian"
```

Run the playbook again and confirm the conditional task ran (or correctly skipped, if you're targeting a non-Debian host):
```bash
ansible-playbook webservers.yml
```
Look for `skipping` vs `changed`/`ok` next to that task in the output — that's Ansible telling you whether the `when` evaluated true.

---

## Part C: Convert a Task to a Template + Handler Pair

Instead of directly copying a static file (as Lab 6 did), use a Jinja2 template so config content can vary, and only reload nginx when that content actually changes.

`templates/index.html.j2`:
```jinja2
<html>
  <body>
    <h1>Configured by Ansible</h1>
    <p>Host: {{ inventory_hostname }}</p>
    <p>Managed users: deploy, monitor</p>
  </body>
</html>
```

Replace Lab 6's `copy` task with:
```yaml
- name: Deploy templated index page
  ansible.builtin.template:
    src: templates/index.html.j2
    dest: /var/www/html/index.html
  notify: Reload nginx

handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
```

Run the playbook twice in a row:
```bash
ansible-playbook webservers.yml
ansible-playbook webservers.yml
```
On the first run, the template task reports `changed` and the handler fires (`Reload nginx` appears in the output). On the second run — nothing in the template changed — the task reports `ok` and **the handler does not run at all**. This is the payoff from today's lecture: the service only restarts when there's an actual reason to.

---

## Part D: Refactor Into a Role

Scaffold a role:
```bash
cd ~/ansible-lab
ansible-galaxy init --init-path roles webserver
```

Move your work into the role's structure:
- The tasks from `webservers.yml` (nginx install, users loop, OS conditional, templated page + handler) go into `roles/webserver/tasks/main.yml`.
- The handler goes into `roles/webserver/handlers/main.yml`.
- The Jinja2 template goes into `roles/webserver/templates/index.html.j2`.

Replace `webservers.yml` with a role call:
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  roles:
    - webserver
```

Run it one more time to confirm the role-based playbook produces the same result as the flat one did:
```bash
ansible-playbook webservers.yml
```

---

## Completion

Show your instructor or TA:
1. The users loop and OS conditional both working (`getent passwd`, and the correct skip/run behavior in the playbook output).
2. Two consecutive `ansible-playbook` runs showing the handler firing on the first run and *not* firing on the second.
3. Your final `roles/webserver/` directory structure (`tasks/`, `handlers/`, `templates/`).
4. The role-based `webservers.yml` producing the same working page as before.
{% endraw %}
