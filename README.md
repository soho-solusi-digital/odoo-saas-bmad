# Odoo SaaS Kit (BMAD Edition)

This project implements a robust SaaS management system for Odoo 18, following the **BMAD (Breakthrough Method for Agile AI Driven Development)** methodology. It provides a complete solution for selling Odoo instances as a service.

## 🚀 Features

Target features (matching or exceeding commercial alternatives):
- **Subscription Management**: Recurring billing cycles (Monthly/Yearly).
- **Automated Provisioning**: Zero-touch instance creation using Docker/Containerization.
- **Domain Mapping**: Support for custom domains with automated SSL (Let's Encrypt).
- **User-Based Pricing**: Dynamic billing based on user count and usage.
- **Client Portal**: Self-service portal for customers to manage their instances (Restart, Backup, Restore).
- **Trial Management**: Automated trial periods with expiration handling.
- **Backup & Disaster Recovery**: Automated scheduled backups and one-click restore.

## 🛠️ Architecture

Built using the BMAD method for clean, scalable code.

- **Models**: Separated concerns (Plan, Contract, Instance, Server).
- **Controllers**: API endpoints for instance communication.
- **Views**: Clean backend UI and responsive customer portal.
- **Docker Integration**: Uses Docker SDK for Python to manage containers.

## 📦 Installation & Usage

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL
- Odoo 18 Source (saas-18 branch)

### Setup

1. **Clone the Project**
   ```bash
   git clone https://github.com/your-repo/odoo-saas-bmad.git
   cd odoo-saas-bmad
   ```

2. **Prepare Environment**
   Ensure Docker is running and accessible by the current user.

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Odoo**
   ```bash
   ./odoo-bin -c config/odoo.conf
   ```

5. **Install Module**
   - Go to Apps -> Update App List.
   - Search for "Odoo SaaS Kit (BMAD)".
   - Click Install.

## 📚 BMAD Methodology
This project adheres to the BMAD principles:
- **Modular Design**: Each feature is loosely coupled.
- **AI-Driven Development**: Code generated and optimized by AI agents.
- **Continuous Documentation**: Documentation evolves with the code.
