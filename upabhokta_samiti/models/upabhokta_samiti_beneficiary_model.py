from odoo import fields, models, api


class UpabhoktaSamitiBeneficiaryModel(models.Model):
    _name = "upabhokta.samiti.beneficiary.record"
    _description = "Upabhokta samiti beneficiary model"
    _rec_name = "category"

    category = fields.Many2one("upabhokta.samiti.beneficiary.master")
    category_male_population = fields.Char("Male Population")
    category_female_population = fields.Char("Female Population")
    category_family_numbers = fields.Char("Family Number")

    page_ref = fields.Many2one("upabhokta.samiti.info")
