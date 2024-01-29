from odoo import models, fields, api

class Documents(models.Model):
    _name = "documents"
    _description = "Documents"
    _rec_name = "doc_name"

    doc_name = fields.Char("Documentation Name") 
    doc_file = fields.Binary("File")