# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class odoo_dev_test_jala(models.Model):
#     _name = 'odoo_dev_test_jala.odoo_dev_test_jala'
#     _description = 'odoo_dev_test_jala.odoo_dev_test_jala'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
