# -*- coding: utf-8 -*-
# from odoo import http


# class OdooDevTestJala(http.Controller):
#     @http.route('/odoo_dev_test_jala/odoo_dev_test_jala', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_dev_test_jala/odoo_dev_test_jala/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_dev_test_jala.listing', {
#             'root': '/odoo_dev_test_jala/odoo_dev_test_jala',
#             'objects': http.request.env['odoo_dev_test_jala.odoo_dev_test_jala'].search([]),
#         })

#     @http.route('/odoo_dev_test_jala/odoo_dev_test_jala/objects/<model("odoo_dev_test_jala.odoo_dev_test_jala"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_dev_test_jala.object', {
#             'object': obj
#         })
