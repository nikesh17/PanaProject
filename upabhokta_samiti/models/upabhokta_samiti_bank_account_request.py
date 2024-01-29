from odoo import api, fields, models


class BankOpeningRequest(models.Model):
    _name = "upabhokta.samiti.project.bankreq"
    _description = "Upabhokta Samiti Bank Opening Request Model "
    _rec_name = "document_name"

    bank_request_doc_text = fields.Html(string=" Bank Opening Request Format")
    signed_document = fields.Binary(string="Signed Document")
    document_name = fields.Char("Document Name")
    page_ref = fields.Many2one("upabhokta.samiti.info")
    
