##############################################
# Internet Gateway (for public subnet)
##############################################

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "custom-vpc-igw"
  }
}

##############################################
# NAT Gateway (so private subnets can reach
# internet for updates, but stay unreachable
# from outside)
##############################################

resource "aws_eip" "nat_eip" {
  domain = "vpc"

  tags = {
    Name = "nat-eip"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public.id   # NAT must sit in the PUBLIC subnet

  tags = {
    Name = "custom-vpc-nat"
  }

  depends_on = [aws_internet_gateway.igw]
}
