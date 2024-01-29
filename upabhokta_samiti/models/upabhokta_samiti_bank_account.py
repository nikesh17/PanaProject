from odoo import api, fields, models


class UpabhoktaSamitiBankAccount(models.Model):
    _name = "upabhokta.samiti.bank.account"
    _description = "Upabhokta Samiti Bank Account"
    _rec_name = "bank_name"

    bank_name = fields.Char(string="Bank Name")
    bank_location = fields.Char(string="Bank Location")
    bank_account = fields.Char(string="Bank Account")

    # page ref
    bank_details_id = fields.Many2one("upabhokta.samiti.info")
