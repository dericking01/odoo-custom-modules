from odoo import models, fields, api # type: ignore

class SalesReport(models.Model):
    _name = 'sales.reporting'
    _description = 'Sales Reporting'

    customer_id = fields.Many2one('res.partner', string='Customer')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def get_filtered_sales(self):
        domain = []
        if self.customer_id:
            domain.append(('partner_id', '=', self.customer_id.id))
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))

        sales_orders = self.env['sale.order'].search(domain)
        return sales_orders