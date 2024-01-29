from odoo import fields,models

class ToleBikashDecision(models.Model):
    _name="tole.bikash.decision"
    _description = "Tole Bikash Decision"

    decision_name = fields.Char("Decision Name")
    decision_detail = fields.Html("Decision Detail")
    decision_document = fields.Binary("Decision Document", attachment=True)
    decision_id = fields.Many2one('tole.bikash.info')
    