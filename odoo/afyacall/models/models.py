# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api # type: ignore


class afyacall(models.Model):
    _name = 'afyacall.afyacall'
    _description = 'these are Afyacall products'

    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables Chatter tracking

    name = fields.Char(string="Name", tracking=True)
    product_id = fields.Integer()
    price = fields.Float(string="Price", digits=(16, 2), required=True,  tracking=True)
    afyacall_customer_id = fields.Many2one('res.partner', string="Overseed By", tracking=True)
    description = fields.Text(string="Description")
    source = fields.Selection(
        string='source',
        selection=[
            ('hot', 'Hot'),
            ('warm', 'Warm'),
            ('cold', 'Cold')
        ],
        help="Type is used to separate Leads and Opportunities",
        default='hot'
    )


class groups(models.Model):
    _name = 'afyacall.groups'
    _description = 'These are Afyacall Groups'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # ✅ Enables chatter & activities

    name = fields.Char(required=True, tracking=True)
    numbers = fields.Integer(tracking=True)
    expired_at = fields.Date(string='Expired At', compute='_compute_expired_at', store=True, tracking=True)
    description = fields.Text(tracking=True)
    created_by = fields.Many2one('res.partner', string='Partner', tracking=True)
    
    status = fields.Selection(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('pending', 'Pending')
        ],
        default='pending',
        tracking=True
    )

    retention = fields.Selection(
        string='Retention Period',
        selection=[
            ('7', '7 days'),
            ('14', '14 days'),
            ('30', '30 days')
        ],
        tracking=True
    )

    contact_count = fields.Integer(string='Contact Count', compute='_compute_contact_count', store=True)
    group_contact_ids = fields.One2many('afyacall.contacts', 'group_id', string='Contacts')

    @api.depends('group_contact_ids')
    def _compute_contact_count(self):
        for group in self:
            group.contact_count = len(group.group_contact_ids)

    @api.depends('retention')
    def _compute_expired_at(self):
        for record in self:
            if record.retention:
                retention_days = int(record.retention)
                record.expired_at = fields.Date.today() + timedelta(days=retention_days)
            else:
                record.expired_at = False

    def action_log_activity(self):
        """Logs an activity when an action is performed"""
        for record in self:
            record.message_post(body=f"📢 A new activity has been logged for group: **{record.name}**")



class contacts(models.Model):
    _name = 'afyacall.contacts'
    _description = 'these are Afyacall contacts'    

    contacts = fields.Char()
    group_id = fields.Many2one('afyacall.groups', string='Group')    

    _sql_constraints = [
    ('unique_contacts', 'unique(contacts)', 'The contact must be unique!')
]

