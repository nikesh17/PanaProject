from odoo import fields,models

class ToleBikashProposal(models.Model):
    _name="tole.bikash.proposal"
    _description = "Tole Bikash Proposal"

    proposal_name = fields.Char("Proposal Name")
    proposal_detail = fields.Html("Proposal Detail")
    proposal_document = fields.Binary("Proposal Document")

    proposal_id = fields.Many2one('tole.bikash.info')

