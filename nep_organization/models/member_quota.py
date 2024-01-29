from odoo import fields, models, api


class OrganizationMemberTypeModel(models.Model):
    _name = "organization.member.quota"
    _description = "Organization Member Type model"
    _rec_name = "category"

    category = fields.Many2one("quota.master")
    category_total_numbers = fields.Integer("Total Number")
    # member_male_population = fields.Integer("Male Population")
    # member_female_population = fields.Integer("Female Population")
    # member_other_population = fields.Integer("Other Population")
    member_total_numbers = fields.Integer("Total Number")
    page_ref = fields.Many2one("organization.information")

