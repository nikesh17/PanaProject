from odoo import api, fields, models


class UpabhoktaSamitiConfig(models.Model):
    _name = "upabhokta.samiti.config"
    _description = "Upabhokta Samiti configurations"


class OrganizationDesignationRepresentative(models.Model):
    _name = "organization.designation.representative"
    _rec_name = "organization_representative_designations"

    organization_representative_designations = fields.Char(
        string="Representative Designation"
    )


class OrganizationDesignationOrganization(models.Model):
    _name = "organization.designation.organization"
    _rec_name = "organization_samiti_designations"

    organization_samiti_designations = fields.Char(string="Samiti Member Designation")


class YojanaType(models.Model):
    _name = "org.yojana.type"
    _rec_name = "yojana_type"

    yojana_type = fields.Char(string="Yojana Type")


class BudgetType(models.Model):
    _name = "org.budget.type"
    _rec_name = "budget_type"

    budget_type = fields.Char(string="Budget Type")


class UpabhoktaSamitiCategory(models.Model):
    _name = "upabhokta.samiti.category"
    _rec_name="category"

    category = fields.Char(string="Upabhokta Samiti Category")
