from odoo import fields, models, api


class OrganizationBeneficiaryMasterModel(models.Model):
    _name = "organization.beneficiary.master"
    _description = "Organization beneficiary master"
    _rec_name="category_name"

    category_name = fields.Char("Beneficiary Category Name")
