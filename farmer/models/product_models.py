from odoo import models,fields,_,api

class ProductsTemplate(models.Model):
    _inherit = 'product.template'
    _description= 'Product Template Model'

    def _get_default_company(self):
        if "allowed_company_ids" in dict(self.env.context).keys():
            res = self.env.context["allowed_company_ids"][0]
        else:
            res = 1
        res = self.env["res.company"].search([('id','=',res)])[0]
        return res

    def _get_default_parent_company(self):
        if "allowed_company_ids" in dict(self.env.context).keys():
            res = self.env.context["allowed_company_ids"][0]
        else:
            res = 1
        res = self.env["res.company"].search([('id','=',res)])[0]
        return res.parent_id

    my_company_id = fields.Many2one("res.company","Associated Company",default=_get_default_company)
    parent_company_id = fields.Many2one("res.company","Associated Company",default=_get_default_parent_company)