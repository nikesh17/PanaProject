# -*- coding: utf-8 -*-
# from odoo import http


# class TaxMeasurement(http.Controller):
#     @http.route('/tax_measurement/tax_measurement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_measurement/tax_measurement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_measurement.listing', {
#             'root': '/tax_measurement/tax_measurement',
#             'objects': http.request.env['tax_measurement.tax_measurement'].search([]),
#         })

#     @http.route('/tax_measurement/tax_measurement/objects/<model("tax_measurement.tax_measurement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_measurement.object', {
#             'object': obj
#         })
