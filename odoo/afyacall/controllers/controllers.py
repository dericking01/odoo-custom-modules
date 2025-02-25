# -*- coding: utf-8 -*-
# from odoo import http


# class Afyacall(http.Controller):
#     @http.route('/afyacall/afyacall', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/afyacall/afyacall/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('afyacall.listing', {
#             'root': '/afyacall/afyacall',
#             'objects': http.request.env['afyacall.afyacall'].search([]),
#         })

#     @http.route('/afyacall/afyacall/objects/<model("afyacall.afyacall"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('afyacall.object', {
#             'object': obj
#         })
