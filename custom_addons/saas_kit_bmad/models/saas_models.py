# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import logging
import docker
import socket

_logger = logging.getLogger(__name__)

class SaasServer(models.Model):
    _name = 'saas.server'
    _description = 'Docker Host Server'
    
    name = fields.Char(required=True)
    host = fields.Char(string='Host IP', required=True, default='localhost', help='Use "unix:///var/run/docker.sock" for local')
    port = fields.Integer(string='Port', default=2375)
    domain = fields.Char(string='Base Domain', help='e.g., saas.my-domain.com')
    is_master = fields.Boolean(default=False)
    
    active = fields.Boolean(default=True)

    def _get_docker_client(self):
        """ Establish connection to Docker Engine """
        try:
            if self.host.startswith('unix://'):
                return docker.DockerClient(base_url=self.host)
            else:
                base_url = f"tcp://{self.host}:{self.port}"
                return docker.DockerClient(base_url=base_url)
        except Exception as e:
            raise exceptions.UserError(f"Failed to connect to Docker: {str(e)}")

class SaasInstance(models.Model):
    _name = 'saas.instance'
    _description = 'Odoo Instance (Container)'

    name = fields.Char(string='Instance Name', required=True)
    domain = fields.Char(string='Full Domain', required=True)
    server_id = fields.Many2one('saas.server', string='Server', required=True)
    container_id = fields.Char(string='Container ID', readonly=True)
    
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

    def action_create_container(self):
        """ Provision Docker Container """
        self.status = 'creating'
        client = self.server_id._get_docker_client()
        
        try:
            # 1. Pull Image (if needed)
            image_name = "odoo:16.0" # Make this configurable later
            try:
                client.images.get(image_name)
            except docker.errors.ImageNotFound:
                _logger.info(f"Pulling image {image_name}...")
                client.images.pull(image_name)

            # 2. Configure Environment
            env = {
                "HOST": "db", # Assuming standard docker-compose network
                "USER": self.db_user or "odoo",
                "PASSWORD": self.db_password or "odoo"
            }

            # 3. Create & Run Container
            container = client.containers.run(
                image_name,
                detach=True,
                name=self.name,
                environment=env,
                labels={"saas.instance": self.name},
                network="odoo-saas-network", # Need to ensure this network exists
                restart_policy={"Name": "always"}
            )
            
            self.container_id = container.id
            self.status = 'running'
            _logger.info(f"Container {self.name} created successfully.")
            
        except Exception as e:
            self.status = 'error'
            _logger.error(f"Failed to create container: {str(e)}")
            raise exceptions.UserError(f"Container creation failed: {str(e)}")

    def action_start(self):
        if not self.container_id:
            return self.action_create_container()
            
        client = self.server_id._get_docker_client()
        container = client.containers.get(self.container_id)
        container.start()
        self.status = 'running'

    def action_stop(self):
        if not self.container_id:
            return
            
        client = self.server_id._get_docker_client()
        container = client.containers.get(self.container_id)
        container.stop()
        self.status = 'stopped'

    def action_restart(self):
        if not self.container_id:
            return
            
        client = self.server_id._get_docker_client()
        container = client.containers.get(self.container_id)
        container.restart()
        self.status = 'running'

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
