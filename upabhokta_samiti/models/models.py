from odoo import fields, models


class UpabhoktaSamitiMaster(models.Model):
    _name = "upabhokta.samiti.master"

    user_id = fields.Integer()

    info_id = fields.Integer()
    bhela_id = fields.Integer()
    formation_member_create_uid = fields.Integer()
    beneficiary_create_uid = fields.Integer()
    proposal_id = fields.Integer()
    attendees_create_uid = fields.Integer()
    bank_account_create_uid = fields.Integer()
    bank_request_create_uid = fields.Integer()
    anugaman_create_uid = fields.Integer()
    registration_date = fields.Datetime(default=fields.Datetime.now)
    registration_number = fields.Char()
    is_verified = fields.Boolean(default=True)
