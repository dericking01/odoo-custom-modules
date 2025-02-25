from odoo import models, fields, api # type: ignore

class FundRequestRejectWizard(models.TransientModel):
    _name = 'fund.request.reject.wizard'
    _description = 'Fund Request Rejection Wizard'

    reason = fields.Text(string="Rejection Reason", required=True)

    def action_reject(self):
        fund_request = self.env['fund.request'].browse(self._context.get('active_id'))
        fund_request.write({
            'state': 'rejected',
            'approval_comments': self.reason,
        })

        # Log the rejection reason in the chatter
        fund_request.message_post(body=f"Fund Request Rejected. Reason: {self.reason}")
        
        return {'type': 'ir.actions.act_window_close'}        
