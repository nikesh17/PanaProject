from odoo.http import request
from odoo.exceptions import AccessDenied,ValidationError
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class ResUsers(models.Model):
    _inherit = 'res.users'

    prefered_keyboard = fields.Many2one("user.keyboard")