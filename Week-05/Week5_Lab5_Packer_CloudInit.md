# Lab 5: Packer & Cloud-Init

Today's required work is Cloud-Init: configuring an instance at boot time from an already-built image (Part C/D). Building that image yourself with Packer (Part A/B) is an optional stretch goal for anyone who wants the practice — not required for completion. You'll get a pre-built AMI ID from your instructor to use either way.

## Prerequisites
- AWS CLI and Terraform both working (Labs 3-4).
- The AMI ID for today's lab (from your instructor or the course LMS).
- Only if attempting the optional stretch goal: `packer -version` returning a version ≥ 1.10.

---

## Part A/B (Optional Stretch Goal): Build Your Own Image

Not required — skip straight to **Part C** if you're using the provided AMI. This section is here for anyone who wants hands-on practice writing and running a Packer build themselves.

### Part A: Write a Packer Template

Create `nginx.pkr.hcl`:
```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "acit4640-nginx-{{timestamp}}"
  instance_type = "t2.micro"
  region        = "us-west-2"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      virtualization-type = "hvm"
    }
    owners      = ["099720109477"]
    most_recent = true
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl enable nginx"
    ]
  }
}
```

### Part B: Build the Image

```bash
packer init .
packer validate nginx.pkr.hcl
packer build nginx.pkr.hcl
```
Note the AMI ID Packer prints when the build finishes. Confirm it in the AWS console under **EC2 → AMIs**. Use this AMI ID in Part D instead of the provided one.

---

## Part C: Write a Cloud-Init user-data Script

Create `cloud-init.yaml`:
```yaml
#cloud-config
runcmd:
  - systemctl start nginx
  - echo "Configured by cloud-init - $(hostname)" > /var/www/html/index.html
```
This assumes nginx is already installed on the image — pre-baked in, whether that's the AMI your instructor provided or the one you built yourself in the optional stretch goal. Cloud-Init here only handles what should vary per-instance: starting the service and writing a per-instance page.

## Part D: Launch and Verify

```bash
AMI_ID=<the AMI ID your instructor provided, or your own from the optional stretch goal>

aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type t2.micro \
  --key-name my_aws_key \
  --security-group-ids <your-SG-from-Lab-3> \
  --subnet-id <your-subnet-from-Lab-3> \
  --associate-public-ip-address \
  --user-data file://cloud-init.yaml \
  --count 1
```
Wait a minute for Cloud-Init to run, then visit the instance's public IP in a browser. You should see your custom page — with no manual SSH configuration involved.

---

## Cleanup

```bash
# terminate the instance
aws ec2 terminate-instances --instance-ids <instance-id>
```

**Only if you did the optional stretch goal** and built your own AMI — the provided AMI is shared across the class, do not deregister it:
```bash
aws ec2 deregister-image --image-id "$AMI_ID"
aws ec2 describe-snapshots --owner-ids self \
  --query "Snapshots[?Description contains 'acit4640-nginx'].SnapshotId" --output text
aws ec2 delete-snapshot --snapshot-id <snapshot-id-from-above>
```
Deregistering an AMI does **not** automatically delete its snapshot — leaving orphaned snapshots is a common source of surprise storage charges.

---

## Completion

Show your instructor or TA:
1. The launched instance serving your custom page in a browser.
2. Confirmation that your instance is terminated.
3. **If you did the optional stretch goal:** your own AMI visible in the AWS console (before cleanup), and confirmation it's since been deregistered with its snapshot deleted.
