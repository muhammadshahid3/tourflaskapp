##############################################
# DB Subnet Group - spans both private subnets
##############################################

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "rds-subnet-group"
  }
}

##############################################
# RDS Instance (MySQL) - Private Subnets only
##############################################

resource "aws_db_instance" "mysql_db" {
  identifier             = "myapp-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = false   # stays private - not reachable from internet
  skip_final_snapshot    = true    # ok for dev/learning, NOT for production

  tags = {
    Name = "private-rds"
  }
}
