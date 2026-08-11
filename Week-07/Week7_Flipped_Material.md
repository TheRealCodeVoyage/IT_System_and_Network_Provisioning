# Week 7 Flipped Material

**Complete this before Week 9's class.** Week 8 is a scheduled break — no class, no new reading due that week. Quiz7, at the start of Week 9, covers today's session (including the infrastructure-types discussion) plus this reading.

## Introduction to Terraform Variables & Modules

So far every Terraform configuration you've written has been one flat file with values hardcoded directly into it. That doesn't scale past a single environment. Variables and modules are how Terraform configurations become reusable.

- **Read:** the official Terraform documentation on [Input Variables](https://developer.hashicorp.com/terraform/language/values/variables) — focus on declaring a variable, referencing it with `var.name`, and setting values via `.tfvars` files, the CLI, or environment variables.
- **Read:** the official Terraform documentation on [Modules](https://developer.hashicorp.com/terraform/language/modules) — focus on what a module is, why you'd extract one, and how a root module calls a child module with a `module` block.

Come to Week 9 ready to answer: why would a team wrap a Terraform configuration in a module instead of copy-pasting the same `.tf` file into a new folder for every environment?

---
*Reminder: Quiz7, at the start of Week 9, draws on this reading and today's Week 7 session (review + physical/virtual/container discussion).*
