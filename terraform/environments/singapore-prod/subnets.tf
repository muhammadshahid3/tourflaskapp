##############################################
# Subnets: 1 Public + 2 Private
##############################################

# Public subnet - EC2 will live here
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block               = var.public_subnet_cidr
  availability_zone        = var.azs[0]
  map_public_ip_on_launch  = true   # instances here auto-get a public IP

  tags = {
    Name = "public-subnet"
  }
}

# Private subnet 1 - RDS (AZ-a)
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[0]
  availability_zone = var.azs[0]

  tags = {
    Name = "private-subnet-1"
  }
}

# Private subnet 2 - RDS (AZ-b) - RDS needs subnets in 2 different AZs
resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[1]
  availability_zone = var.azs[1]

  tags = {
    Name = "private-subnet-2"
  }
}
