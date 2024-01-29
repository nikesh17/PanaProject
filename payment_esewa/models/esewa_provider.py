from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from datetime import datetime
import requests
import pprint
import logging

_logger = logging.getLogger(__name__)


class EsewaProvider(models.Model):
    _inherit = 'payment.provider'

    merchant_code= fields.Char("Merchant Code",default="EPAYTEST")
    domain_name = fields.Char(_("Server Domain"),default="http://localhost")
    port=fields.Char(_("Port Number"),default="8069")
    code = fields.Selection(
        selection_add=[('esewa', "esewa")], ondelete={'esewa': 'set default'}
    )
    # esewa_auth_key=fields.Char(string='Esewa Authorization Key', required_id_provider="esewa", groups='base.group_system')


