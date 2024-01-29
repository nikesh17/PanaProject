from odoo.http import request
from odoo.exceptions import AccessDenied,ValidationError
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class Keyboards(models.Model):
    _name = 'user.keyboard'

    name = fields.Char(string=_("Name"))
    char_map = fields.Char(string=_("Charater Map"))
    post_rules = fields.Char(string=_("Post Rules"))