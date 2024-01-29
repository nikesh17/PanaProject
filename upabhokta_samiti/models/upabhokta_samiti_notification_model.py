from odoo import fields, models


class UpabhoktaSamitiNotificationModel(models.Model):
    _name = "upabhokta.samiti.notification"

    status = fields.Boolean("Status", default=False)
    message = fields.Char("Message")
    sent_by = fields.Many2one("res.users")
    sent_to = fields.Many2one("res.users")
    sent_at = fields.Datetime("Sent at",default=fields.Datetime.now())

    