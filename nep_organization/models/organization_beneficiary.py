from odoo import fields, models, api


class OrganizationBeneficiaryModel(models.Model):
    _name = "organization.beneficiary.record"
    _description = "Organization beneficiary model"
    _rec_name = "category"

    category = fields.Many2one("organization.beneficiary.master")
    category_male_population = fields.Char("Male Population")
    category_female_population = fields.Char("Female Population")
    category_family_numbers = fields.Char("Family Number")

    page_ref = fields.Many2one("organization.information")
