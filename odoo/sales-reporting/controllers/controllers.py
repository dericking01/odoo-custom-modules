# -*- coding: utf-8 -*-
# from odoo import http


# class Sales-reporting(http.Controller):
#     @http.route('/sales-reporting/sales-reporting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales-reporting/sales-reporting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales-reporting.listing', {
#             'root': '/sales-reporting/sales-reporting',
#             'objects': http.request.env['sales-reporting.sales-reporting'].search([]),
#         })

#     @http.route('/sales-reporting/sales-reporting/objects/<model("sales-reporting.sales-reporting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales-reporting.object', {
#             'object': obj
#         })
