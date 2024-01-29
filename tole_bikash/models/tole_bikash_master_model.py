from odoo import fields, models


class ToleBikashMaster(models.Model):
    _name = "tole.bikash.master"

    user_id = fields.Integer()
    info_id = fields.Integer()
    meeting_id = fields.Integer()
    member_formation_id = fields.Integer()
    proposal_id = fields.Integer()
    decision_id = fields.Integer()
    attendees_create_uid = fields.Integer()
    registration_date = fields.Datetime(default=fields.Datetime.now)
    registration_number = fields.Char()
    is_verified = fields.Boolean(default=True)
