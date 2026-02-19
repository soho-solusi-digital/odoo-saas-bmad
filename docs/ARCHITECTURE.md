# Architecture & Design

## 1. Overview
The Odoo SaaS Kit (BMAD) manages multi-tenant Odoo instances as a service. It orchestrates the lifecycle of containers, databases, and subscriptions, allowing for a fully automated SaaS business.

## 2. Core Modules
- **`saas.plan`**: Defines pricing, limits, and configurations for subscription tiers.
- **`saas.contract`**: Manages the subscription relationship with the customer.
- **`saas.instance`**: Represents a deployed Odoo instance (container/database).
- **`saas.server`**: Represents the physical or virtual server hosting the instances (Docker host).

## 3. Workflow (BMAD)
1. **Purchase**: Customer buys a plan via the website.
2. **Contract Creation**: A `saas.contract` is generated.
3. **Provisioning**: The system triggers instance creation on a `saas.server` via Docker API.
4. **Running**: The instance becomes available at a subdomain (e.g., `client1.saas.com`).
5. **Billing**: Recurring invoices are generated based on usage.
6. **Self-Service**: Customer manages backups/restarts via the portal.

## 4. Technical Stack
- **Backend**: Odoo 18 (Python)
- **Containerization**: Docker (API via `docker` python library)
- **Database**: PostgreSQL (Multi-tenant schema or separate DBs per instance)
- **Proxy**: Nginx (Automated vhost configuration)
- **SSL**: Let's Encrypt (Certbot automation)

## 5. Security
- Isolated containers per client.
- Secure database credentials management.
- Restricted access to Docker socket.
