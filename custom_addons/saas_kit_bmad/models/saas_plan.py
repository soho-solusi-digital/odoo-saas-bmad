# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaasPlan(models.Model):
    _name = 'saas.plan'
    _description = 'Subscription Plan (BMAD)'
    
    name = fields.Char('Plan Name', required=True)
    price = fields.Float('Monthly Price')
    max_users = fields.Integer('Max Users')
    storage_limit = fields.Float('Storage (GB)')
    trial_period_days = fields.Integer('Trial Period (Days)')
    
    server_ids = fields.Many2many('saas.server', string='Deployment Servers')
