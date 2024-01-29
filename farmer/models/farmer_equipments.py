from odoo import models, fields,api,_
import qrcode
import nepali_datetime
import base64
from io import BytesIO
from odoo.exceptions import ValidationError
from . import organization_model


class EquipmentType(models.Model):
    _name = 'farm.equipment.type'
    _description = 'Equipment type'

    name = fields.Char(string=_('Equipment Type'))

class Equipment(models.Model):
    _name = 'farm.equipment'

    farmer_id = fields.Many2one('farm.farmer',string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group',string=_('Farmer'))
    name = fields.Char(string=_("Name"))
    is_rented = fields.Boolean(string=_("Is rented"))
    capacity = fields.Char(string=('Ability'))
    quantity = fields.Integer(string=_('Quantity'))
    equipment_type = fields.Many2one('farm.equipment.type',string=_('Equipment Type'))

class ConstructionType(models.Model):
    _name = 'farm.construction.type'
    _description = 'construction type'

    name = fields.Char(string=_('Construction Type'))


class Construction(models.Model):
    _name = 'farm.construction'

    farmer_id = fields.Many2one('farm.farmer',string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group',string=_('Farmer'))
    construction_type = fields.Many2one('farm.construction.type',string=_('Construction Type'))
    quantity = fields.Integer(string=_('Quantity'))
    area = fields.Float(string=_('area'))