# 🧭 TourApp — AWS Infrastructure & Deployment

![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?logo=terraform)
![AWS](https://img.shields.io/badge/AWS-Singapore-orange?logo=amazonaws)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![MySQL](https://img.shields.io/badge/RDS-MySQL%208.0-4479A1?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)

A Flask-based tour/travel booking application deployed on AWS (Singapore region) using a custom VPC, EC2, and RDS — provisioned with Terraform and containerized with Docker.

Built as an end-to-end demonstration of shipping a real web app on real, hand-rolled cloud infrastructure — not just "code that works," but a network designed the way production systems actually are: public-facing app tier, locked-down private data tier, and everything reproducible from a single `terraform apply`.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Security](#security)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
- [Local Development](#local-development)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Notes](#notes)
- [License](#license)

## Overview

This project provisions a production-style AWS network from scratch and deploys a Flask application on top of it:

- Custom VPC with public + private subnets
- EC2 instance running the Flask app inside Docker
- RDS (MySQL) database in private subnets, reachable only from the app server
- All infrastructure defined as code with Terraform

## Features

**User-facing**
- Browse tours by category and destination
- Search tours with filters
- User signup/login with session-based auth
- Book tours and view booking history
- Personal dashboard and profile management

**Admin panel**
- Separate admin signup/login
- Manage tours, categories, and destinations (CRUD)
- View and manage all bookings
- Reports dashboard for booking/revenue insights
- Manage registered users

**Infrastructure**
- Fully reproducible AWS environment via Terraform
- Isolated network tiers (public app, private data)
- Dockerized app for consistent deployment across environments

## Architecture

```
                        Internet
                            │
                    ┌───────▼────────┐
                    │ Internet Gateway│
                    └───────┬────────┘
                            │
        ┌───────────────────────────────────┐
        │        VPC — 10.0.0.0/16            │
        │                                     │
        │   ┌─────────────────────────┐       │
        │   │  Public Subnet (10.0.1.0/24)      │
        │   │  ┌─────────────────┐    │       │
        │   │  │  EC2 (Ubuntu)    │    │       │
        │   │  │  Docker: Flask   │    │       │
        │   │  └────────┬─────────┘    │       │
        │   └───────────┼──────────────┘       │
        │               │                       │
        │   ┌───────────▼──────────────┐        │
        │   │  Private Subnets (AZ-a / AZ-b)     │
        │   │  RDS MySQL (private only)          │
        │   └─────────────────────────┘         │
        └───────────────────────────────────┘
```

| Component | Detail |
|---|---|
| Region | ap-southeast-1 (Singapore) |
| VPC | 10.0.0.0/16 |
| Public subnet | 10.0.1.0/24 — hosts the EC2 app server |
| Private subnets | 10.0.2.0/24, 10.0.3.0/24 — hosts RDS (multi-AZ) |
| EC2 | Ubuntu 22.04, Docker + Docker Compose |
| RDS | MySQL 8.0, `publicly_accessible = false` |
| App | Flask, containerized |

## Security

- EC2 security group: SSH restricted to an allow-listed IP, HTTP open for the app
- RDS security group: only accepts traffic from the EC2 security group — the database has no route from the public internet at all
- Private subnets reach the internet outbound (for OS updates) via a NAT Gateway, but accept no inbound traffic from outside the VPC

## Tech Stack

- **Infrastructure:** Terraform
- **Compute:** AWS EC2 (Ubuntu 22.04)
- **Database:** AWS RDS (MySQL 8.0)
- **App:** Flask, run via Docker Compose
- **Containerization:** Docker

## Repository Structure

```
tourapp/
├── terraform/              # infrastructure as code (VPC, EC2, RDS, SGs)
├── docker-compose.yml      # runs the Flask app container
├── Dockerfile
├── app/                    # Flask application code
└── .env.example            # sample environment variables (DB connection, etc.)
```

## Prerequisites

Make sure you have these installed/set up before deploying:

- [ ] AWS account with programmatic access (Access Key + Secret Key)
- [ ] [Terraform](https://developer.hashicorp.com/terraform/downloads) `>= 1.5`
- [ ] [AWS CLI](https://aws.amazon.com/cli/) configured (`aws configure`)
- [ ] An EC2 key pair created in `ap-southeast-1` (Singapore) for SSH access
- [ ] Docker & Docker Compose (installed automatically on EC2 in the steps below, or locally if you want to run the app without AWS)
- [ ] Git

## Deployment Steps

### 1. Provision infrastructure

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # fill in real values
terraform init
terraform apply
```

### 2. SSH into the EC2 instance

```bash
ssh -i tourapp ubuntu@<ec2-public-ip>
```

### 3. Install Docker on EC2

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
```

### 4. Clone the app and configure environment

```bash
git clone <repo-url> && cd tourapp
cp .env.example .env   # set DB_HOST to the RDS endpoint, plus credentials
```

### 5. Build and run the app

```bash
docker compose up -d --build
```

### 6. Verify the database connection

```bash
docker compose exec app python manage.py migrate   # or your app's equivalent
```

## Local Development

Want to run the app without spinning up AWS? You can run it fully locally with Docker Compose and a local MySQL container:

```bash
git clone <repo-url> && cd tourapp
cp .env.example .env          # point DB_HOST to "db" (the compose service name)
docker compose up -d --build
```

Then visit `http://localhost:5000` (or whichever port is mapped in `docker-compose.yml`).

To run outside Docker entirely, using a virtualenv:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run
```

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DB_HOST` | RDS endpoint (or `db` for local Docker) | `tourapp.xxxxx.ap-southeast-1.rds.amazonaws.com` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_NAME` | Database name | `tourapp` |
| `DB_USER` | Database username | `admin` |
| `DB_PASSWORD` | Database password | `********` |

```
DB_HOST=<rds-endpoint>
DB_PORT=3306
DB_NAME=tourapp
DB_USER=<db-username>
DB_PASSWORD=<db-password>
```

## Troubleshooting

**Can't SSH into EC2**
Check that your IP is still in the allow-list on the EC2 security group — Terraform hardcodes it via `terraform.tfvars`, and if your IP changed (new network, VPN), you'll need to update it and re-apply.

**App can't reach the database**
Confirm the RDS security group only allows inbound traffic from the EC2 security group (not a CIDR block), and that `DB_HOST` in `.env` exactly matches the RDS endpoint from `terraform output`.

**`terraform apply` fails on VPC limits**
Some AWS accounts cap VPCs per region (default is often 5). Check existing VPCs in `ap-southeast-1` or request a limit increase.

**Docker Compose fails to build**
Run `docker compose logs app` to see the actual stack trace — most commonly a missing environment variable or a dependency not pinned in `requirements.txt`.

## Roadmap

- [ ] HTTPS via ACM + Application Load Balancer
- [ ] CI/CD pipeline (GitHub Actions) for automated Terraform plan/apply and Docker image builds
- [ ] Move RDS credentials to AWS Secrets Manager
- [ ] Auto Scaling Group instead of a single EC2 instance
- [ ] CloudWatch alarms and centralized logging

## Contributing

Contributions are welcome! To propose a change:

1. Fork the repo and create a feature branch (`git checkout -b feature/your-feature`)
2. Make your changes and test locally
3. Commit with a clear message and open a Pull Request

Please avoid committing `.env`, `terraform.tfstate`, or any private keys.

## Notes

- `terraform.tfstate`, private SSH keys, and `.env` files are intentionally excluded from version control — see `.gitignore`.
- RDS is deployed with `skip_final_snapshot = true`, which is fine for a demo/learning environment but should be revisited before production use.

## License

This project is licensed under the [MIT License](LICENSE).