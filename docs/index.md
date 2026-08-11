---
title: "ACIT 4640: IT Systems and Network Provisioning"
---

# ACIT 4640: IT Systems and Network Provisioning

Labs and flipped-material readings for BCIT's ACIT 4640, in the Computer Information Technology (CIT) diploma program. The course moves from manual system administration to Infrastructure as Code, working across physical, virtual, and cloud environments.

Everything students need for hands-on work lives here. Slides, quizzes, tests, and exams are distributed through the course LMS, not this site.

## Labs Index

| # | Lab | Week |
|---|---|---|
| 1 | [Local Development Environment Setup](labs/Lab_01.html) | Week 1 |
| 2 | [SSH, Bash Scripting, and Service Management](labs/Lab_02.html) | Week 2 |
| 3 | [AWS CLI — Authentication, Networking, and Your First EC2 Instance](labs/Lab_03.html) | Week 3 |
| 4 | [Terraform Basics](labs/Lab_04.html) | Week 4 |
| 5 | [Packer & Cloud-Init](labs/Lab_05.html) | Week 5 |
| 6 | [Introduction to Ansible](labs/Lab_06.html) | Week 6 |
| 7 | [Terraform Variables & Modules](labs/Lab_07.html) | Week 9 |
| 8 | [Ansible Loops, Conditionals, Handlers & Roles](labs/Lab_08.html) | Week 10 |
| 9 | [Bare-Metal Provisioning with PXE](labs/Lab_09.html) | Week 11 |
| 10 | [Migrating to an S3 Remote Backend](labs/Lab_10.html) | Week 12 |

## Flipped Material Index

Each week's reading is assigned **during** that week and is meant to be completed **before the next class**. The topic listed is what the reading prepares you for.

| Assigned | Reading | Prepares you for |
|---|---|---|
| Week 1 | [Week 1 Flipped Material](flipped-material/Week_01.html) | Bash variables, environment variables & command substitution |
| Week 2 | [Week 2 Flipped Material](flipped-material/Week_02.html) | Introduction to the AWS CLI |
| Week 3 | [Week 3 Flipped Material](flipped-material/Week_03.html) | Introduction to Terraform |
| Week 4 | [Week 4 Flipped Material](flipped-material/Week_04.html) | Introduction to Packer |
| Week 5 | [Week 5 Flipped Material](flipped-material/Week_05.html) | Introduction to Ansible |
| Week 6 | [Week 6 Flipped Material](flipped-material/Week_06.html) | Physical vs. virtualized vs. containerized infrastructure |
| Week 7 | [Week 7 Flipped Material](flipped-material/Week_07.html) | Terraform variables & modules |
| Week 9 | [Week 9 Flipped Material](flipped-material/Week_09.html) | Ansible flow control, roles & collections |
| Week 10 | [Week 10 Flipped Material](flipped-material/Week_10.html) | How network booting works: DHCP, TFTP, and the PXE chain |
| Week 11 | [Week 11 Flipped Material](flipped-material/Week_11.html) | Terraform state management & remote backends |
| Week 12 | [Week 12 Flipped Material](flipped-material/Week_12.html) | Final exam preparation |

*Week 8 is a scheduled break, and Week 13 is a review session — neither has a lab or an assigned reading.*

## Course Overview

ACIT 4640 introduces the concepts, processes, and tools used to automatically provision IT infrastructure and deploy applications. Students work with physical, virtual, and containerized runtime environments, both on-premises and on a public cloud provider (AWS).

### Learning Outcomes

By the end of this course, students will be able to:

1. Provision Linux operating systems using DHCP, PXE, TFTP, and preconfigured installers.
2. Write imperative scripts to provision and configure virtualized services on a local host.
3. Describe the relative advantages of physical, virtualized, and containerized infrastructure.
4. Enumerate, compare, select, and use popular configuration management and provisioning tools.
5. Understand and describe the infrastructure required to deploy and run a web service in production.
6. Write declarative code to provision and configure infrastructure and virtualized services on a local host.
7. Write code to automate the configuration of base images using Cloud-Init and user-data.
8. Write declarative code to provision and configure infrastructure and services on a public cloud.
9. Manage all Infrastructure as Code artifacts using modern version control.

### Technical Stack

- **Operating system:** Debian / Ubuntu (via WSL2 or a local VM)
- **Containers:** Incus (system containers)
- **Cloud provider:** Amazon Web Services
- **Provisioning:** Terraform, Packer
- **Configuration management:** Ansible, Cloud-Init
- **Bare metal:** DHCP, TFTP, PXE
- **Version control:** Git / GitLab
- **Languages:** Bash, HCL, YAML

## Getting Started

Start with [Lab 1](labs/Lab_01.html), which sets up the Linux environment, editor, version control, and container runtime that every later lab depends on. Complete it before Week 2 — the labs build on each other, and a broken environment in Week 1 becomes a broken lab in Week 5.
