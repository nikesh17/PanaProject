from odoo import api, fields, models


class OrganizationPurpose(models.Model):
    _name = "organization.purpose"
    _description = "Organization Purpose model"
    _rec_name = "document_name"

    purpose_text = fields.Html(string="Organization Purpose")
    signed_document = fields.Binary(string="Signed Document")
    document_name = fields.Char("Document Name")
    page_ref = fields.Many2one("organization.information")
    
