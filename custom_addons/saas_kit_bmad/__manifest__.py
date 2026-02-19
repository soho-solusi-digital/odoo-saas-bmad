{
  "name": "Odoo SaaS Kit (BMAD)",
  "version": "18.0.1.0.0",
  "category": "SaaS",
  "summary": "BMAD Method Implementation of Odoo SaaS Kit",
  "description": """
      BMAD Implementation of Odoo SaaS Kit.
      Features:
      - Subscription Management
      - Automated Instance Provisioning (Docker)
      - Domain Mapping & SSL
      - User-based Pricing
      - Client Portal
  """,
  "author": "Koda",
  "depends": ["base", "sale_management", "website", "account", "portal", "mail"],
  "data": [
      "security/ir.model.access.csv",
      "views/saas_menu.xml",
      "views/saas_plan_views.xml",
  ],
  "installable": True,
  "application": True,
  "license": "LGPL-3"
}
