from odoo import api, fields, models


class ProjectProposal(models.Model):
    _name = "upabhokta.samiti.project.proposal"
    _description = "Upabhokta Samiti Project Proposal model"
    _rec_name = "document_name"

    proposal_text = fields.Html(string="Project Proposal")
    signed_document = fields.Binary(string="Signed Document")
    document_name = fields.Char("Document Name")
    page_ref = fields.Many2one("upabhokta.samiti.info")
    
