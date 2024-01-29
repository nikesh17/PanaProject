from odoo import fields, models, api


class UpabhoktaSamitiBeneficiaryMasterModel(models.Model):
    _name = "upabhokta.samiti.beneficiary.master"
    _description = "Upabhokta samiti beneficiary master"
    _rec_name="category_name"

    category_name = fields.Char("Beneficiary Category Name")
