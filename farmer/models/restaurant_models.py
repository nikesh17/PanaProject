from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import tools

class RestFloorInherit(models.Model):
    _inherit='restaurant.floor'

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

    parent_company_id = fields.Many2one("res.company","Associated Company",default=_get_default_parent_company)
    company_id = fields.Many2one("res.company","Associated Company",default=_get_default_company)