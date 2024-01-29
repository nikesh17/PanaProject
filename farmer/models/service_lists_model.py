from odoo import models, fields, _


class ServiceLists (models.Model):
    _inherit = 'fis.base.model'
    _name = 'services.lists'
    _description = 'Services Lists'

    name = fields.Char(string=_('Service Lists'))


class EquipmentLists (models.Model):
    _inherit = 'fis.base.model'
    _name = 'equipment.lists.model'
    _description = 'Equipment Lists'

    name = fields.Char(string=_('Equipment Lists'))


class FishLarvaLists (models.Model):
    _inherit = 'fis.base.model'
    _name = 'fish_larva.lists.model'
    _description = 'Fish Larva Lists'

    name = fields.Char(string=_('Fish Larva Lists'))



