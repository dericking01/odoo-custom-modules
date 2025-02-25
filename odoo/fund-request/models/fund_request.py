from odoo import models, fields, api # type: ignore
from odoo.exceptions import UserError # type: ignore

class FundRequest(models.Model):
    _name = 'fund.request'
    _description = 'Fund Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables chatter for logging activities

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    amount = fields.Float(string="Amount", required=True)
    department_id = fields.Many2one('hr.department', string="Department", related='employee_id.department_id', store=True)
    purpose = fields.Text(string="Purpose", required=True, tracking=True)
    approval_comments = fields.Text(string="Manager's comments")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='draft', tracking=True)

    manager_id = fields.Many2one('res.users', string="Approved By", readonly=True)
    is_editable = fields.Boolean(string="Is Editable", compute='_compute_is_editable', store=False) # Computed field to check if the record is editable

    @api.depends('state')  # Only depends on the 'state' field
    def _compute_is_editable(self):
        for record in self:
            # If the state is 'approved', only managers can edit
            if record.state == 'approved':
                record.is_editable = self.env.user.has_group('hr.group_hr_manager')
            else:
                record.is_editable = True
    
    def write(self, vals):
        """ Move back to draft when an employee edits a rejected request """
        if self.state == 'rejected' and any(field in vals for field in ['employee_id', 'department_id', 'amount', 'purpose']):
            vals['state'] = 'draft'
        return super(FundRequest, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fund.request') or 'New'
        return super(FundRequest, self).create(vals)

    # Submit request
    def action_submit(self):
        self.write({'state': 'submitted'})

    # Approve request
    def action_approve(self):
        if not self.env.user.has_group('hr.group_hr_manager'):  # Ensure only HR managers approve
            raise UserError("Only managers can approve requests.")
        self.write({'state': 'approved', 'manager_id': self.env.user.id})

    # Reject request
    def action_reject(self):
        self.write({'state': 'rejected'})

    # method to open the wizard instead of directly rejecting the request.
    def action_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reject Fund Request',
            'res_model': 'fund.request.reject.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('fund-request.view_fund_request_reject_wizard_form').id,  # Ensure the correct module name
            'target': 'new',
            'context': {'default_fund_request_id': self.id},
        }
