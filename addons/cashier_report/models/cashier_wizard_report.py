from odoo import models, fields, api

class CashierReportWizard(models.TransientModel):
    _name = "cashier.report.wizard"
    _description = "Periodic Cashier Report Wizard"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    shop_id = fields.Many2one('res.company', string="Shop")
    sale_type = fields.Selection([
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail')
    ], string="Sale Type")
    employee_id = fields.Many2one('hr.employee', string="Cashier")  # <-- Added Employee

    total_sales = fields.Monetary(string="Total Sales", readonly=True)
    total_expenditure = fields.Monetary(string="Total Expenditure", readonly=True)
    balance = fields.Monetary(string="Balance", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)

    @api.onchange('start_date', 'end_date', 'shop_id', 'sale_type', 'employee_id')
    def compute_totals(self):
        domain = [('date', '>=', self.start_date), ('date', '<=', self.end_date)]
        if self.shop_id:
            domain.append(('shop_id', '=', self.shop_id.id))
        if self.sale_type:
            domain.append(('sale_type', '=', self.sale_type))
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))  # <-- Filter by employee

        reports = self.env['cashier.report'].search(domain)
        self.total_sales = sum(reports.mapped('total_sales'))
        self.total_expenditure = sum(reports.mapped('total_expenditure'))
        self.balance = self.total_sales - self.total_expenditure
