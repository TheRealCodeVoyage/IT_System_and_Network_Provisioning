# Week 11 Flipped Material

**Complete this before Week 12's class.** Quiz10 at the start of Week 12 covers this reading plus today's PXE session.

## Terraform State Management & Remote Backends

Every Terraform command you've run this term has stored its state in a single local file, `terraform.tfstate`, sitting in your project directory. That works fine solo, but breaks down the moment more than one person — or more than one machine — needs to run `terraform apply` against the same infrastructure.

- **Read:** the official Terraform documentation on [State](https://developer.hashicorp.com/terraform/language/state) — focus on what state actually tracks, and why two people applying from two different local state files is dangerous.
- **Read:** the official Terraform documentation on [Backends](https://developer.hashicorp.com/terraform/language/backend) — focus on what a backend does and why a remote backend (like an S3 bucket) solves the local-file problem.

Come to Week 12 ready to answer: what specifically goes wrong if two team members each run `terraform apply` from their own laptop, both pointed at the same local `terraform.tfstate` copy?

---
*Reminder: Quiz10, at the start of Week 12, draws on this reading and today's Week 11 session (PXE / bare-metal provisioning).*
