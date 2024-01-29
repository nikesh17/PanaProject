# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tax_measurement(models.Model):
#     _name = 'tax_measurement.tax_measurement'
#     _description = 'tax_measurement.tax_measurement'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
