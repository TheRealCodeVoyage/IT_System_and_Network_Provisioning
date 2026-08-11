---
title: "Week 6 Flipped Material"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Week 6 Flipped Material

**Complete this before Week 7's class.** Next week is lighter on new hands-on material — it's built around Test 2 plus a class discussion, not a new lab. Quiz6 at the start of Week 7 covers this reading plus today's Ansible lecture.

## Physical vs. Virtualized vs. Containerized Infrastructure

All term we've provisioned virtual machines in AWS. Before Week 13's PXE demo puts a physical machine in front of you, it's worth stepping back and comparing the three infrastructure types this course touches: physical (bare metal), virtualized (what we've been using), and containerized.

- **Read:** Red Hat's [Containers vs. virtual machines](https://www.redhat.com/en/topics/containers/containers-vs-vms) explainer (or an equivalent overview of your choosing — the goal is walking into Wednesday's discussion with a working sense of the trade-offs, not a specific source).

Come to class ready to discuss: what does each infrastructure type cost you in terms of setup time, isolation, density, and portability? Where does each one make sense?

### Live demo preview

In class, we'll put this into practice: you already installed Incus back in Week 1 (Lab 1), so we'll relaunch a container live and set it side by side against a VM you've already built this term (an EC2 instance, or your Lab 9 VirtualBox VM once we reach it), to see the setup-time/isolation/density trade-offs directly instead of just reading about them.

```bash
incus launch images:debian/13 demo
incus list
incus exec demo -- systemctl status
```

Feel free to run this yourself beforehand if you want a head start on the discussion — it's the same commands from Lab 1, just a fresh container.

---
*Reminder: Quiz6, at the start of Week 7, draws on this reading and today's Ansible lecture. Test 2 also happens next week, covering Weeks 4–6.*
{% endraw %}
