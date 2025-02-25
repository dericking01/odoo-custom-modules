# -*- coding: utf-8 -*-
# from odoo import http


# class Fund-request(http.Controller):
#     @http.route('/fund-request/fund-request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fund-request/fund-request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fund-request.listing', {
#             'root': '/fund-request/fund-request',
#             'objects': http.request.env['fund-request.fund-request'].search([]),
#         })

#     @http.route('/fund-request/fund-request/objects/<model("fund-request.fund-request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fund-request.object', {
#             'object': obj
#         })
