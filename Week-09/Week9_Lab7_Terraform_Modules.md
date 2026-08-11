# Lab 7: Terraform Variables & Modules

Today you'll take the security group + EC2 instance pair you built by hand in Lab 4 and turn it into a reusable module — then call that module twice with different inputs, proving the same code can stand up two differently-configured instances.

## Prerequisites
- Lab 4 completed (or your `main.tf` from it available to reference).
- `terraform -version` returning a version ≥ 1.10.

---

## Part A: Project Layout

Create a fresh project directory with a `modules/` subdirectory:
```bash
mkdir -p ~/terraform-lab7/modules/web_instance
cd ~/terraform-lab7
```

You should end up with this structure:
```
terraform-lab7/
├── main.tf
├── provider.tf
└── modules/
    └── web_instance/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## Part B: Write the Module

`modules/web_instance/variables.tf`:
```hcl
variable "instance_name" {
  type        = string
  description = "Value for the instance's Name tag"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type to launch"
  default     = "t2.micro"
}

variable "allowed_ssh_cidr" {
  type        = string
  description = "CIDR block allowed to SSH into the instance"
}
```

`modules/web_instance/main.tf`:
```hcl
resource "aws_security_group" "this" {
  name        = "acit4640-${var.instance_name}-sg"
  description = "Allow SSH from a specific CIDR"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  ami                    = "ami-xxxxxxxxxxxxxxxxx" # a recent Ubuntu 22.04 AMI in us-west-2
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.this.id]

  tags = {
    Name = "acit4640-${var.instance_name}"
  }
}
```

`modules/web_instance/outputs.tf`:
```hcl
output "instance_id" {
  description = "The launched instance's AWS resource ID"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "The launched instance's public IP address"
  value       = aws_instance.this.public_ip
}
```

Notice this is exactly Lab 4's security group and instance — the only change is that every value that used to be hardcoded (`acit4640-lab4-sg`, `t2.micro`, the tag name) is now a variable.

---

## Part C: Call the Module Twice

`provider.tf`:
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

`main.tf`, in the project root (not inside `modules/`):
```hcl
module "web_a" {
  source            = "./modules/web_instance"
  instance_name     = "lab7-web-a"
  instance_type     = "t2.micro"
  allowed_ssh_cidr  = "YOUR_IP_HERE/32"
}

module "web_b" {
  source            = "./modules/web_instance"
  instance_name     = "lab7-web-b"
  instance_type     = "t3.micro"
  allowed_ssh_cidr  = "YOUR_IP_HERE/32"
}

output "web_a_ip" {
  value = module.web_a.public_ip
}

output "web_b_ip" {
  value = module.web_b.public_ip
}
```

Two calls to the same module, two different instance types, two different names — zero duplicated resource blocks.

---

## Part D: Plan, Apply, and Verify

```bash
terraform init
terraform fmt
terraform validate
terraform plan
```
Confirm the plan shows **four** resources being created (two security groups, two instances) and **two** module outputs.

```bash
terraform apply
```
Type `yes` when prompted.

Once applied:
```bash
terraform output
```
You should see `web_a_ip` and `web_b_ip`, each populated with a real public IP — pulled from inside the module through its `outputs.tf`, not hardcoded anywhere in your root config.

---

## Cleanup

```bash
terraform destroy
```
Type `yes` when prompted. Confirm both instances are gone in the AWS console (or with `aws ec2 describe-instances`).

---

## Completion

Show your instructor or TA:
1. Your `modules/web_instance/` directory (`main.tf`, `variables.tf`, `outputs.tf`).
2. `terraform plan` showing 4 resources across 2 module calls.
3. `terraform output` showing both `web_a_ip` and `web_b_ip` populated after `apply`.
4. `terraform destroy` completing successfully, with no resources left running.
