# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaasServer(models.Model):
    _name = 'saas.server'
    _description = 'Server Configuration'
    
    name = fields.Char(required=True)
    host = fields.Char(string='Host', required=True, default='localhost')
    port = fields.Integer(string='Port', default=8069)
    domain = fields.Char(string='Base Domain', help='e.g., saas.my-domain.com')
    is_master = fields.Boolean(default=False)
    
    active = fields.Boolean(default=True)

class SaasInstance(models.Model):
    _name = 'saas.instance'
    _description = 'Odoo Instance (Container/DB)'

    name = fields.Char(string='Instance Name', required=True)
    domain = fields.Char(string='Domain', required=True)
    server_id = fields.Many2one('saas.server', string='Server', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('creating', 'Creating'),
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('error', 'Error'),
    ], default='draft', string='Status')

    db_name = fields.Char(string='Database Name')
    db_user = fields.Char(string='DB User')
    db_password = fields.Char(string='DB Password')
    
    plan_id = fields.Many2one('saas.plan', string='Subscription Plan')
    contract_id = fields.Many2one('saas.contract', string='Contract')

    def action_start(self):
        # Placeholder for start logic
        self.status = 'running'

    def action_stop(self):
        # Placeholder for stop logic
        self.status = 'stopped'

    def action_restart(self):
        self.action_stop()
        self.action_start()

    def action_backup(self):
        # Placeholder for backup logic
        pass

    def action_restore(self):
        # Placeholder for restore logic
        pass

class SaasContract(models.Model):
    _name = 'saas.contract'
    _description = 'Subscription Contract'
    
    name = fields.Char(string='Reference', required=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    plan_id = fields.Many2one('saas.plan', string='Plan', required=True)
    instance_id = fields.Many2one('saas.instance', string='Instance')
    
    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    
    def action_confirm(self):
        # Trigger instance creation
        self.state = 'active'
        self._create_instance()

    def _create_instance(self):
        # Implementation to create saas.instance
        vals = {
            'name': f"{self.plan_id.name}-{self.id}",
            'domain': f"{self.id}.saas.local",
            'server_id': self.plan_id.server_ids[:1].id, # Simple allocation
            'plan_id': self.plan_id.id,
            'contract_id': self.id,
        }
        self.env['saas.instance'].create(vals)
