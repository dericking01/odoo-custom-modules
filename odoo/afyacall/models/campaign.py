from datetime import timedelta
from odoo import models, fields, api # type: ignore
from odoo.exceptions import UserError # type: ignore

class Campaigns(models.Model):
    _name = 'afyacall.campaigns'
    _description = 'These are Afyacall campaigns'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # ✅ Enables chatter & activities

    campaign_name = fields.Char(required=True, tracking=True)
    message = fields.Text(tracking=True)
    delivery = fields.Text() 
    created_by = fields.Many2one('res.partner', string='Partner', tracking=True)
    groups = fields.Many2many('afyacall.groups', string='Groups', tracking=True)
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
    planned_time = fields.Datetime(string='Planned Time', tracking=True)

    def action_start_campaign(self):
        """Start the campaign and log a note"""
        for record in self:
            if not record.message:
                raise UserError("You cannot start a campaign without a message!")

            if not record.groups:
                raise UserError("Please select at least one group for the campaign.")

            # Update status
            record.status = 'active'

            # Log a note in the chatter
            record.message_post(body=f"✅ Campaign **'{record.campaign_name}'** has been started!")

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Campaign started successfully!",
                'type': 'rainbow_man',
            }
        }
   