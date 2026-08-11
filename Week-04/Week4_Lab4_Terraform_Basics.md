# Lab 4: Terraform Basics

Today you'll build the same kind of infrastructure you created by hand in Lab 3 — but declaratively. If you're moving quickly, terminate your Lab 3 resources first (or use a different name/CIDR) to avoid conflicts.

## Prerequisites
- AWS CLI configured with the `acit4640_admin` profile (Lab 3) — Terraform reuses these credentials automatically.
- `terraform -version` returning a version ≥ 1.10.

---

## 1. Initialize Your Project

Create a project directory and a `main.tf` file:
```bash
mkdir ~/terraform-lab4 && cd ~/terraform-lab4
nano main.tf
```

Add a provider block. Terraform will pick up your AWS credentials the same way the CLI does — no keys go in this file:
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
```

Initialize the working directory:
```bash
terraform init
```
This downloads the AWS provider plugin into a hidden `.terraform` directory.

---

## 2. Write Your Configuration

Add a security group and an EC2 instance to `main.tf`:

```hcl
resource "aws_security_group" "lab4_sg" {
  name        = "acit4640-lab4-sg"
  description = "Allow SSH from my IP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP_HERE/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "lab4_web" {
  ami                    = "ami-xxxxxxxxxxxxxxxxx" # a recent Ubuntu 22.04 AMI in us-west-2
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.lab4_sg.id]

  tags = {
    Name = "acit4640-lab4"
  }
}
```
Find a current Ubuntu 22.04 AMI ID for `us-west-2` with the AWS CLI, the same way you did in Lab 3's AMI lookup — or check the AWS console.

Notice `aws_security_group.lab4_sg.id` — this is the dot-notation reference from today's lecture, connecting the instance to the security group you just defined above it.

### Format and Validate
```bash
terraform fmt
terraform validate
```
Run both after any edit — `fmt` keeps your style consistent, `validate` catches syntax errors before you waste time on a plan.

---

## 3. Plan and Apply

```bash
terraform plan
```
Read the plan output before doing anything else. Confirm it's only creating the two resources you expect — nothing more, nothing unexpected.

```bash
terraform apply
```
Type `yes` when prompted.

---

## 4. Inspect State

```bash
cat terraform.tfstate | less
```
Find the two resources you created and identify:
- The instance's assigned AWS resource ID (not something you specified — Terraform got it from AWS).
- The dependency relationship between the instance and the security group.

Also try:
```bash
terraform show
```
This renders the state file in a more human-readable format than the raw JSON.

**Do not hand-edit `terraform.tfstate`** — this is for inspection only.

---

## 5. Clean Up

```bash
terraform destroy
```
Type `yes` when prompted. Confirm in the AWS console (or with `aws ec2 describe-instances`) that the instance is actually gone.

---

## Completion

Show your instructor or TA:
1. `terraform apply` completing successfully, with your instance visible in the AWS console.
2. Your `terraform.tfstate` file, with the instance and security group resources identified.
3. `terraform destroy` completing successfully, with no resources left running.
