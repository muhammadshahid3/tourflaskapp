##############################################
# Latest Ubuntu 22.04 LTS AMI (auto-lookup)
##############################################

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]   # Canonical's official AWS account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

##############################################
# Auto-import your local public key into AWS
# (reads tourapp.pub from this same folder)
##############################################

resource "aws_key_pair" "generated_key" {
  key_name   = var.key_name
  public_key = file("./tourapp.pub")
}

##############################################
# EC2 Instance - Public Subnet
##############################################

resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  key_name                    = aws_key_pair.generated_key.key_name
  associate_public_ip_address = true

  tags = {
    Name = "tourapp"
  }
}