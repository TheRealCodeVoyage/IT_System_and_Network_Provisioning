---
title: "Lab 3: AWS CLI — Authentication, Networking, and Your First EC2 Instance"
---

[&larr; Back to course index]({{ '/' | relative_url }})

{% raw %}
# Lab 3: AWS CLI — Authentication, Networking, and Your First EC2 Instance

This lab moves you from managing local Linux environments to managing public cloud infrastructure with the AWS CLI. By the end, you'll have authenticated the CLI, built a minimal network from scratch, launched an EC2 instance into it, connected over SSH using last week's key, and cleaned everything up again.

## Prerequisites
- A functional local Linux development environment (Lab 1).
- Your SSH key pair from Lab 2.
- An active AWS account.

---

## Task 1: Create an IAM User for CLI Access

Before the CLI can do anything, it needs a way to authenticate.

1. Log in to the AWS Management Console and navigate to **IAM**.
2. Go to **Users → Add users**. Name the user `acit4640_admin`.
3. Attach the `AdministratorAccess` policy. *(In production you'd follow least-privilege instead — we use Admin here so IaC tools aren't blocked by permissions mid-lab.)*
4. Open the new user, go to **Security credentials → Create access key**, and choose **Command Line Interface (CLI)** as the use case.
5. **Download the `.csv` file.** You will only see the Secret Access Key once. Keep it secure — never commit it to a git repository, email it, or post it anywhere.

---

## Task 2: Install and Configure the AWS CLI

### Install AWS CLI v2
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version   # should start with aws-cli/2.x.x
```

### Configure a Named Profile
```bash
aws configure --profile acit4640_admin
```
Provide the Access Key ID and Secret Access Key from your `.csv`, region `us-west-2`, and output format `json`.

Set this profile as your default so you don't need `--profile` on every command:
```bash
echo 'export AWS_PROFILE=acit4640_admin' >> ~/.bashrc
source ~/.bashrc
```

**Verify authentication:**
```bash
aws sts get-caller-identity
```

---

## Task 3: Build a Minimal VPC

```bash
# Create the VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
  --query 'Vpc.VpcId' --output text)
aws ec2 create-tags --resources "$VPC_ID" --tags Key=Name,Value=acit4640-vpc

# Create a public subnet
SUBNET_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 \
  --availability-zone us-west-2a --query 'Subnet.SubnetId' --output text)
aws ec2 modify-subnet-attribute --subnet-id "$SUBNET_ID" --map-public-ip-on-launch

# Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"

# Route table: send all internet-bound traffic through the IGW
RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id "$RT_ID" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
aws ec2 associate-route-table --route-table-id "$RT_ID" --subnet-id "$SUBNET_ID"
```
Notice the pattern: each command's `--query`'d output feeds directly into the next command via command substitution — the exact technique from Week 2's flipped material.

---

## Task 4: Security Group, Launch, and SSH In

```bash
# Security group: allow SSH from your IP only
SG_ID=$(aws ec2 create-security-group --group-name acit4640-sg \
  --description "Lab 3 SG" --vpc-id "$VPC_ID" --query 'GroupId' --output text)
MYIP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" \
  --protocol tcp --port 22 --cidr "${MYIP}/32"

# Import last week's public key as an EC2 key pair
aws ec2 import-key-pair --key-name my_aws_key \
  --public-key-material fileb://~/.ssh/my_aws_key.pub

# Find a recent Ubuntu 22.04 AMI
AMI_ID=$(aws ec2 describe-images --owners 099720109477 \
  --filters 'Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*' \
  --query 'Images | sort_by(@,&CreationDate) | [-1].ImageId' --output text)

# Launch the instance into your new VPC
INSTANCE_ID=$(aws ec2 run-instances --image-id "$AMI_ID" --instance-type t2.micro \
  --key-name my_aws_key --security-group-ids "$SG_ID" --subnet-id "$SUBNET_ID" \
  --associate-public-ip-address --count 1 \
  --query 'Instances[0].InstanceId' --output text)
aws ec2 create-tags --resources "$INSTANCE_ID" --tags Key=Name,Value=acit4640-lab3

# Wait for it to be running, then grab its public IP
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Instance is up at: $PUBLIC_IP"
```

Update the `Host aws-instance` entry in `~/.ssh/config` from Lab 2 with this IP, then connect:
```bash
ssh -i ~/.ssh/my_aws_key ubuntu@${PUBLIC_IP}
```

---

## Task 5: Clean Up

Leaving resources running is the most common way to rack up unexpected AWS charges — tear everything down in dependency order once you've confirmed SSH access works.

```bash
aws ec2 terminate-instances --instance-ids "$INSTANCE_ID"
aws ec2 wait instance-terminated --instance-ids "$INSTANCE_ID"
aws ec2 delete-security-group --group-id "$SG_ID"
aws ec2 detach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"
aws ec2 delete-internet-gateway --internet-gateway-id "$IGW_ID"
aws ec2 delete-subnet --subnet-id "$SUBNET_ID"
aws ec2 delete-route-table --route-table-id "$RT_ID"
aws ec2 delete-vpc --vpc-id "$VPC_ID"
```
Save the cleanup commands into a `cleanup.sh` script rather than running them ad hoc — you'll want it again in future labs.

---

## Completion

Show your instructor or TA:
1. `aws sts get-caller-identity` returning your `acit4640_admin` identity.
2. Your EC2 instance reachable over SSH (screen share the connection).
3. Your `cleanup.sh` script, and confirmation the VPC and its resources are gone (`aws ec2 describe-vpcs` shouldn't list it).
{% endraw %}
