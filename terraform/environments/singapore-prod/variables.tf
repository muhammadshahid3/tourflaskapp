##############################################
# Variables (edit values in terraform.tfvars)
##############################################

variable "aws_region" {
  description = "AWS region - Singapore"
  type        = string
  default     = "ap-southeast-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the whole VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidrs" {
  description = "CIDRs for the 2 private subnets"
  type        = list(string)
  default     = ["10.0.2.0/24", "10.0.3.0/24"]
}

variable "azs" {
  description = "Availability zones to use in ap-southeast-1"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name to give the EC2 key pair in AWS (auto-created from your .pub file)"
  type        = string
  default     = "tourapp-key"
}

variable "my_ip" {
  description = "Your IP address in CIDR form, e.g. 1.2.3.4/32 (used to allow SSH only from you)"
  type        = string
  default     = "0.0.0.0/0"   # <-- WARNING: yeh sabko SSH allow karta hai. Apna IP daal kar zyada mehfooz karein
}

variable "db_name" {
  description = "Initial database name"
  type        = string
  default     = "mydb"
}

variable "db_username" {
  description = "Master username for RDS"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Master password for RDS (min 8 chars)"
  type        = string
  sensitive   = true
  default     = "pX9!mK4#vL7$zQ2["   # <-- apna password yahan daal dein
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}