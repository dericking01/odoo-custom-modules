from odoo import models, fields, api # type: ignore
import xlsxwriter # type: ignore
import base64
from io import BytesIO

class SalesReportingWizard(models.TransientModel):
    _name = 'sales.reporting.wizard'
    _description = 'Sales Reporting Wizard'

    customer_ids = fields.Many2many(
        'res.partner',  # Model name
        string='Customers',  # Field label
        domain="[('customer_rank', '>', 0)]"  # Optional: Filter only customers
    )
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_export_excel(self):
        # Filter sales orders based on the wizard inputs
        domain = []
        if self.customer_ids:
            domain.append(('partner_id', 'in', self.customer_ids.ids))
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))

        sales_orders = self.env['sale.order'].search(domain)

        # Create an Excel file in memory
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sales Orders')

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFF00',  # Yellow background
            'border': 1,            # Add a border
            'align': 'center',      # Center-align text
        })
        data_format = workbook.add_format({
            'border': 1,            # Add a border
            'align': 'left',        # Left-align text
        })

        # Define headers (Subtotal column removed)
        headers = [
            'Order Number', 'Order Date', 'Customer',
            'Product', 'Quantity', 'Unit Price', 'Total Amount'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Write data
        row = 1
        for order in sales_orders:
            # Write order-level information
            worksheet.write(row, 0, order.name, data_format)  # Order Number
            worksheet.write(row, 1, order.date_order.strftime('%Y-%m-%d'), data_format)  # Order Date
            worksheet.write(row, 2, order.partner_id.name, data_format)  # Customer

            # Write order item details
            first_row = row  # Track the first row of the current order
            for line in order.order_line:
                worksheet.write(row, 3, line.product_id.name, data_format)  # Product
                worksheet.write(row, 4, line.product_uom_qty, data_format)  # Quantity
                worksheet.write(row, 5, line.price_unit, data_format)       # Unit Price
                row += 1  # Move to the next row for the next item

            # Write Total Amount
            if order.order_line:
                if len(order.order_line) == 1:
                    # For single-row orders, use worksheet.write
                    worksheet.write(first_row, 6, order.amount_total, data_format)
                else:
                    # For multi-row orders, use merge_range
                    worksheet.merge_range(
                        first_row, 6,  # Start row and column for merging
                        row - 1, 6,    # End row and column for merging
                        order.amount_total,  # Value to write
                        data_format  # Format to apply
                    )

            # Add a blank row between orders for better readability
            row += 1

        # Auto-adjust column widths
        for col, _ in enumerate(headers):
            worksheet.set_column(col, col, max(len(header) for header in headers) + 2)

        workbook.close()
        output.seek(0)
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'detailed_sales_report.xlsx',
            'datas': excel_file,
            'res_model': 'sales.reporting.wizard',
            'res_id': self.id,
            'type': 'binary',
        })

        # Return the action to download the file
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


class SalesReport(models.Model):
    _name = 'sales.reporting'
    _description = 'Sales Reporting'

    def export_to_excel(self, sales_orders):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sales Orders')

        # Write headers
        headers = ['Order Number', 'Customer', 'Date', 'Total Amount']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write data
        for row, order in enumerate(sales_orders, start=1):
            worksheet.write(row, 0, order.name)
            worksheet.write(row, 1, order.partner_id.name)
            worksheet.write(row, 2, order.date_order)
            worksheet.write(row, 3, order.amount_total)

        workbook.close()
        output.seek(0)
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'sales_report.xlsx',
            'datas': excel_file,
            'res_model': 'sales.reporting',
            'res_id': self.id,
            'type': 'binary',
        })

        # Return the action to download the file
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }