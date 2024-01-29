from odoo import models, fields
import nepali_datetime

class OrgRenewalModel(models.Model):
    _name = "organization.renewal"
    _description = "Organization Renewal"

   
    org_reg_number = fields.Char("Registration Number")
    org_registration_date = fields.Char(
        string=" Registration Date"
    )
    issued_province = fields.Many2one(
        "location.province", string=" Issued Province"
    )
    issued_district = fields.Many2one(
        "location.district", string=" Issued District"
    )
    issued_palika = fields.Many2one(
        "location.palika", string=" Issued Municipality"
    ) 
    issued_office = fields.Char("Organization Office Name")
    nabikaran_awadi = fields.Char("Fiscal Year")
    last_nabikaran_date = fields.Char(
        string="Last Nabikaran Date"
    )
    audit_report = fields.Binary("Audit Report", Attachment=True)

    renewal_page_ref = fields.Many2one("organization.information")

   