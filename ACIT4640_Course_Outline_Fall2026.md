# Course Outline

# ACIT 4640
# IT System and Network Provisioning

| | |
|---|---|
| **School** | School of Computing and Academic Studies |
| **Program** | Computer Information Technology |
| **Course Credits** | 4 |
| **Minimum Passing Grade** | 50% |
| **Start Date** | September 8, 2026 |
| **End Date** | December 11, 2026 |
| **Total Hours** | 56 *(verify with the registrar — the 2025 outline listed 60 over 15 weeks; Fall 2026 is a 14-week term)* |
| **Total Weeks** | 14 |
| **Hours/Week** | 4 |
| **Delivery Type** | Lecture |
| **Zero Textbook Cost** | Yes |
| **Prerequisite(s)** | ACIT 2515 and ACIT 2420 and ACIT 3640 |
| **CRN** | *(to be assigned)* |

---

## Acknowledgement of Territories

The British Columbia Institute of Technology acknowledges that our campuses are located on the unceded traditional territories of the Coast Salish Nations of Skwxwú7mesh (Squamish), səlilwətaɬ (Tsleil-Waututh), and xʷməθkʷəy̓əm (Musqueam).

## Instructor Details

| | |
|---|---|
| **Name** | Iman Anooshehpour |
| **E-mail** | *(BCIT address — to be filled in)* |
| **Location** | *(office / campus — to be filled in)* |
| **Office Hours** | By appointment. Please make office-hour appointments at least 24 hours in advance and include what you would like to discuss. See your D2L section for details. |

## Course Description

This course introduces the concepts, processes, and tools used in the automated provisioning of IT infrastructure as well as the deployment of applications using that infrastructure. Students and activities incorporate the management of physical, virtual, and containerized run-time environments both on-premises and in a public cloud. Topics include bare-metal provisioning, scripted installations, containerization, configuration management and provisioning tools.

## Course Learning Outcomes/Competencies

Upon successful completion of this course, the student will be able to:

- Provision Linux operating systems using DHCP, PXE, TFTP, and preconfigured installers.
- Write imperative scripts to provision and configure virtualized services on a local host.
- Describe the relative advantages of physical, virtualized, and containerized infrastructure.
- Enumerate, compare, select and use popular configuration management and provisioning tools.
- Understand and describe the infrastructure required to deploy and run a web service in a production environment.
- Write declarative code to provision and configure infrastructure and virtualized services on a local host.
- Write code to automate the configuration of base images using Cloud-Init and user-data for cloud deployments.
- Write declarative code to provision and configure infrastructure and services on a public cloud.
- Manage all "infrastructure as code" artifacts using modern version control.

## Learning Resources

**Zero textbook cost.** There is no required textbook. All course tools are free or open source.

**Software** — students maintain their own Linux development environment (Debian 13 "trixie" or 14 "forky") via WSL2, a VirtualBox VM, a container, a cloud dev environment, or a native install:

- Git, and a GitHub/GitLab account
- Incus (system containers)
- Terraform / OpenTofu
- Packer
- Ansible
- AWS CLI, with the AWS account provided for the course
- VirtualBox (required for the Week 11 PXE lab)

**Labs and flipped material** are published at <https://therealcodevoyage.github.io/2026-fall-ITSNP/>.

**Slides, quizzes, tests, and exams** are distributed through D2L, not the public site.

**Reference documentation:** [Terraform](https://developer.hashicorp.com/terraform/docs) · [Packer](https://developer.hashicorp.com/packer/docs) · [Ansible](https://docs.ansible.com/) · [AWS CLI](https://docs.aws.amazon.com/cli/latest/) · [Incus](https://linuxcontainers.org/incus/docs/main/) · [cloud-init](https://cloudinit.readthedocs.io/)

## Evaluation Criteria

| Criteria | % | Comments |
|---|---|---|
| Flipped material review | 10 | 10 graded reviews, weighted evenly, to be completed in class. The Week 1 review is ungraded practice. |
| Labs | 15 | 10 labs, weighted evenly, to be completed in class |
| Tests | 45 | 3 tests, 15% each |
| Final exam | 30 | Comprehensive |

**Tests** are written during regular class time. Test coverage always stops one week short of the test date — material introduced in the same week as a test is examined on the final exam instead. More information about the tests will be provided in class.

**Flipped material reviews and labs** are in-class, pass/fail activities. The reviews build conceptual understanding of the assigned pre-class material; the labs build the practical skills for that week's topic. Because both are in-class activities, they cannot be completed remotely or made up after the fact.

Course schedule is subject to change based on class progress. Any changes will be announced in class.

Make-up material for classes that fall on a holiday will be discussed in class.

## Attendance Requirements

Regular attendance in classes is critical to student success, and is monitored. Unsupported absence of 2 or more classes may result in withdrawal from the course or program. Please see [Policy 5101 – Student Regulations](https://www.bcit.ca/about/administration/policies.shtml) and accompanying procedures for more information.

Students are expected to setup and manage their working environment (laptop) by themselves.

## Course Specific Requirements

Some of the tools used in this course have limited macOS and Windows support. Every student must have a working Debian Linux development environment, and maintaining that environment is the student's own responsibility — limited class time is devoted to it. Lab 1 (Week 1) establishes this environment, and every later lab depends on it.

Students should bring a pen or pencil and paper to class for in-class activities.

The Week 11 PXE lab requires VirtualBox and enough disk space and RAM to run two virtual machines simultaneously.

## Course Schedule and Assignments

| Week | Week start | Topics | Assessments |
|---|---|---|---|
| 1 | Sep 07 | Introductions; tooling landscape (Terraform/OpenTofu, Packer, Ansible, Incus); key terminology — provisioning, configuration management, IaC, DevOps; local development environment setup | Flipped material review (ungraded practice)<br>Lab 1 |
| 2 | Sep 14 | Linux review — SSH and key management, Bash scripting, systemd and `systemctl` | Flipped material review<br>Lab 2 |
| 3 | Sep 21 | Public cloud control with the AWS CLI — IAM, CLI configuration and structure, EC2 and VPC | Flipped material review<br>Lab 3 |
| 4 | Sep 28 | Terraform fundamentals — HCL, providers, resources, introduction to state | Test 1 (Weeks 1–3)<br>Flipped material review<br>Lab 4 |
| 5 | Oct 05 | Image building with Packer; just-in-time configuration with Cloud-Init and `user-data`; baked vs. fried images | Flipped material review<br>Lab 5 |
| 6 | Oct 12 | Introduction to Ansible — agentless automation, inventories, ad-hoc commands, playbooks, variables | Flipped material review<br>Lab 6 |
| 7 | Oct 19 | Review and Q&A; physical vs. virtualized vs. containerized infrastructure, with a live Incus container demo | Test 2 (Weeks 4–6)<br>Flipped material review<br>No lab |
| 8 | Oct 26 | No class — scheduled break | — |
| 9 | Nov 02 | Terraform variables and modules | Flipped material review<br>Lab 7 |
| 10 | Nov 09 | Ansible loops, conditionals, handlers, and roles | Flipped material review<br>Lab 8 |
| 11 | Nov 16 | Bare-metal provisioning — DHCP, TFTP, and the PXE boot chain; preconfigured installers; live hardware demo | Test 3 (Week 7 discussion, Weeks 9–10)<br>Flipped material review<br>Lab 9 |
| 12 | Nov 23 | Terraform state management, remote backends (S3), and state locking | Flipped material review<br>Lab 10 |
| 13 | Nov 30 | Course review — Tests 1–3 review and final exam preparation | — |
| 14 | Dec 07 | Final exam week (Dec 7–11) | Final exam |

**Term dates and holidays (Fall 2026):** Labour Day, Sep 7 (classes begin Tue Sep 8) · National Day for Truth and Reconciliation, Wed Sep 30 · Thanksgiving Day, Mon Oct 12 · Remembrance Day, Wed Nov 11 · Withdrawal deadline ("W" on transcript), Nov 13 · Final exams, Dec 7–11.

---

## BCIT Policy

> **Instructor note:** the paragraphs below are institutional boilerplate auto-inserted by BCIT's course-outline system. Do not retype them — paste the current verbatim text from the outline system when publishing. The headings and links are listed here so the section is complete.

The following statements are in accordance with BCIT Policies 5101, 5103, 5104, 5105 and 7507, and their accompanying procedures.

- **Attendance** — [Policy 5101, Student Regulations](https://www.bcit.ca/about/administration/policies.shtml). Students who are absent must contact the instructor or Program Head as soon as possible; supporting documentation may be requested where an absence affects an exam, deadline, or safety requirement.
- **Attempts** — [Policy 5101, Student Regulations](https://www.bcit.ca/about/administration/policies.shtml). A course must be completed within a maximum of three attempts; permission is required before a third attempt.
- **Academic Integrity** — [Policy 5104, Student Code of Academic Integrity](https://www.bcit.ca/about/administration/policies.shtml). Plagiarism, cheating, and gaining unfair academic advantage are prohibited and handled under this policy and its procedures.
- **Accommodation** — [Policy 4501, Accommodation for Students with Disabilities](https://www.bcit.ca/accessibility-services/). Requests go to BCIT Accessibility Services, not to an individual instructor, and should be made as early as possible.
- **Human Rights, Harassment and Discrimination** — [Policy 7507, Harassment and Discrimination](https://www.bcit.ca/about/administration/policies.shtml).

Students should make themselves aware of the additional Education, Administration, Safety, and other BCIT policies listed at <https://www.bcit.ca/about/administration/policies.shtml>.

## Guidelines for School of Computing and Academic Studies

No school specific policies; please refer to main BCIT Policy.

## Approved

I verify that the content of this course outline is current.

Iman Anooshehpour, Instructor
*(date)*

I verify that this course outline has been reviewed.

*(Program Head)*
*(date)*

I verify that this course outline has been reviewed and complies with BCIT policy.

*(Associate Dean)*
*(date)*

---

> **Note:** Students will be given reasonable notice if changes are required in the content of this course outline.
>
> **Total hours — example of 3 credit/instructional hours:**
> - **Full-time master:** 45 hours of scheduled learning
> - **Flexible Learning course:** 30 hours of scheduled learning plus 15 hours of independent, non-instructional learning
