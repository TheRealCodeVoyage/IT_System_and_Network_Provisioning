---
title: "Lab 10: Migrating to an S3 Remote Backend"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Lab 10: Migrating to an S3 Remote Backend

Today you'll take your Lab 7 project (the `web_instance` module, called twice) and move its state from a local file into a locked, shared S3 backend — then prove it actually works by deleting your local Terraform files entirely and rebuilding from nothing but the backend config.

## Prerequisites
- Lab 7 completed, with a working `terraform-lab7/` project (or a fresh copy of it).
- `terraform -version` returning **1.10 or later** — S3-native state locking (`use_lockfile`) requires it. Check now; upgrade first if you're on an older version.

---

## Part A: Create the S3 Bucket

The backend block you'll write in Part B does **not** create the bucket — Terraform expects it to already exist. Create it with a small, separate, one-time configuration using ordinary local state.

```bash
mkdir ~/terraform-lab10-bootstrap && cd ~/terraform-lab10-bootstrap
nano main.tf
```

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "tfstate" {
  bucket = "acit4640-<your-name>-tfstate"  # bucket names must be globally unique

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  versioning_configuration {
    status = "Enabled"
  }
}
```
Replace `<your-name>` with something that makes the bucket name unique to you — S3 bucket names are global across all of AWS, not just your account.

`aws_s3_bucket_versioning` is worth noticing: it keeps prior versions of your state file, so an accidental bad `apply` doesn't destroy your only copy of history.

```bash
terraform init
terraform apply
```
Note the exact bucket name you chose — you'll need it in Part B.

---

## Part B: Add the Backend Block to Your Lab 7 Project

Go back to (or copy) your Lab 7 project:
```bash
cd ~/terraform-lab7
```

Add this to the top of your existing `provider.tf` (alongside the `required_providers` block already there):
```hcl
terraform {
  backend "s3" {
    bucket       = "acit4640-<your-name>-tfstate"
    key          = "lab10/terraform.tfstate"
    region       = "us-west-2"
    encrypt      = true
    use_lockfile = true
  }
}
```
> Your `provider.tf` will now have **two** `terraform { }` blocks worth of content — a `required_providers` block and this new `backend` block. They can be combined into a single `terraform { }` block, or left as two separate ones; both are valid HCL.

---

## Part C: Migrate

```bash
terraform init
```
Terraform will detect the new backend and prompt you to copy your existing local state into it — confirm with `yes`. Watch for the message confirming the backend was successfully initialized.

Verify the state actually landed in S3:
```bash
aws s3 ls s3://acit4640-<your-name>-tfstate/lab10/
```
You should see `terraform.tfstate` listed.

Run a plan to confirm Terraform still recognizes your existing infrastructure — it should show **no changes**, since nothing about the actual resources changed, only where their state lives:
```bash
terraform plan
```

---

## Part D: Prove It — Delete and Rebuild

This is the real test of a working remote backend: your local project directory should be disposable.

```bash
rm -rf .terraform .terraform.lock.hcl
```
> This does **not** touch `terraform.tfstate` locally, because there isn't one anymore — it's been living in S3 since Part C.

Reinitialize from scratch:
```bash
terraform init
```
Terraform re-downloads the provider plugin and reconnects to the existing backend — it does not treat this as a new project with no state.

Confirm your resources are still recognized:
```bash
terraform plan
```
Again: **no changes** expected. If Terraform instead proposes creating your two `web_instance` module calls from scratch, something went wrong reconnecting to the backend — check that your `bucket`, `key`, and `region` values exactly match Part A.

---

## Part E: Observe Locking (Optional but Recommended)

Open two terminals, both `cd`'d into `terraform-lab10`. In the first terminal:
```bash
terraform apply
```
Don't confirm the prompt yet — leave it sitting at `Enter a value:`. In the second terminal, try:
```bash
terraform plan
```
You should see it wait or report that state is locked. Go back to the first terminal and type `no` to cancel — the second terminal's command should then proceed normally. This is the lock file doing its job: preventing a second person (or a second terminal, in this case) from touching state while a change is in flight.

---

## Cleanup

```bash
terraform destroy   # inside terraform-lab7 / terraform-lab10, removes the two web_instance resources
```
Then, from `terraform-lab10-bootstrap`:
```bash
# first empty the bucket of all state versions, since versioning was enabled
aws s3 rm s3://acit4640-<your-name>-tfstate --recursive
terraform destroy   # remove the bucket itself
```

---

## Completion

Show your instructor or TA:
1. `terraform init` successfully migrating local state into your S3 bucket (Part C).
2. `aws s3 ls` confirming `terraform.tfstate` exists inside the bucket.
3. A completely clean `.terraform` directory (deleted), followed by `terraform init` and `terraform plan` showing **no changes** — proof state survived without any local copy.
4. Both S3 buckets destroyed and confirmed empty in the AWS console at the end.
{% endraw %}
