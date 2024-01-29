from odoo import api, fields, models


class OrganizationConfig(models.Model):
    _name = "organization.config"
    _description = "organization configurations"


class OrganizationDesignationRepresentative(models.Model):
    _name = "org.representative.designation"
    _rec_name = "org_representative_designations"

    org_representative_designations = fields.Char(
        string="Representative Designation"
    )

class OrganizationAssetType(models.Model):
    _name = "org.asset.master"
    _rec_name = "org_asset_type"

    org_asset_type = fields.Char(
        string="Asset Type"
    )

class OrganizationAssetType(models.Model):
    _name = "org.asset.master"
    _rec_name = "org_asset_type"

    org_asset_type = fields.Char(
        string="Asset Type"
    )
class OrganizationCategory(models.Model):
    _name = "org.category.master"
    _rec_name = "org_category"

    org_category = fields.Char(
        string="Organization Category"
    )

class OrganizationMemberCategory(models.Model):
    _name = "quota.master"
    _rec_name = "quota"

    quota = fields.Char(
        string="Quota"
    )

class OrganizationMemberQualificationCategory(models.Model):
    _name = "member.qualification.master"
    _rec_name = "member_qualification"

    member_qualification = fields.Char(
        string="Member Category"
    )
class OrgCollaborativeCategory(models.Model):
    _name = "collaborative.org.master"
    _rec_name = "collaborative_org"

    collaborative_org = fields.Char(
        string="Member Category"
    )



