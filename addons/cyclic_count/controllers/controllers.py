# -*- coding: utf-8 -*-
# from odoo import http


# class CyclicCount(http.Controller):
#     @http.route('/cyclic_count/cyclic_count', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cyclic_count/cyclic_count/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cyclic_count.listing', {
#             'root': '/cyclic_count/cyclic_count',
#             'objects': http.request.env['cyclic_count.cyclic_count'].search([]),
#         })

#     @http.route('/cyclic_count/cyclic_count/objects/<model("cyclic_count.cyclic_count"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cyclic_count.object', {
#             'object': obj
#         })

