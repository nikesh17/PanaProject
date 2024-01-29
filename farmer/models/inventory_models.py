from odoo import models,fields,_,api
import nepali_datetime 

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Stock Warehouse'

    parent_company_id = fields.Many2one("res.company","Associated Company",related='company_id.parent_id')
    # Address Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    @api.model
    def create(self, vals):
        return super(StockWarehouse, self).create(vals)