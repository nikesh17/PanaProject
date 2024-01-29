from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import tools

class AccMove(models.Model):
    _inherit='res.partner'


    # Location Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    full_address = fields.Char("Address",compute="_compute_full_address")

    def _compute_full_address(self):
        for record in self:
            temp=""
            if record.palika:
                temp+=record.palika.palika_name
            if record.ward_no:
                temp+=' - '+record.ward_no+', '
            if record.district:
                temp+=record.district.district_name+', '
            if record.province:
                temp+=record.province.name
            
            record.full_address = temp


    @api.model_create_multi
    def create(self, vals):
        res = super(AccMove, self).create(vals)
        property_account_receivable_id = self.env['account.account'].sudo().search([('account_type', '=', 'asset_receivable'), ('deprecated', '=', False), ('company_id', '=', self.env.company.id)],limit=1)
        property_account_payable_id = self.env['account.account'].sudo().search([('account_type', '=', 'liability_payable'), ('deprecated', '=', False), ('company_id', '=', self.env.company.id)],limit=1)

        for rec in res:
            rec.property_account_receivable_id = property_account_receivable_id
            rec.property_account_payable_id = property_account_payable_id
        return res