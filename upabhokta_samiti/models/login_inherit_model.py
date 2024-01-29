from odoo import fields, models


class Signup(models.Model):
    _inherit = "res.users"

    phone = fields.Char("Phone Number")
    # upabhokta_samiti_category = fields.Many2one("upabhokta.samiti.category", default=1)
