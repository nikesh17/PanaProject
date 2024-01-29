from odoo import models,fields,_


class AgricultureActivity (models.Model):
    _inherit = 'fis.base.model'
    _name= 'farmer.agriculture.activities'
    _description= 'Agriculture activities'

    name = fields.Char(string=_('Agriculture Activity'))


class AgricultureSubActivity (models.Model):
    _inherit = 'fis.base.model'
    _name= 'farmer.agriculture.sub.activities'
    _description= 'Agriculture activities'

    parent_id = fields.Many2one("farmer.agriculture.activities",string=_("Agriculture Activity"))
    name = fields.Char(string=_('Agriculture Sub Activity'))


class SeedlingLists (models.Model):
    _inherit = 'fis.base.model'
    _name= 'seedling.lists.model'
    _description= 'Seedling Lists'

    name = fields.Char(string=_('Seedling Lists'))



