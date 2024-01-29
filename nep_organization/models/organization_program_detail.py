from odoo import fields, models, api


class OrganizationProgramDetailModel(models.Model):
    _name = "organization.program.record"
    _description = "OrganizationProgram detail model"
    
    program_name  = fields.Char("Program Name")
    program_purpose = fields.Html("Program Purpose")
    program_chairman_fullname = fields.Char(string="Chairman")
    program_location = fields.Char("Program Location")
    program_start_time = fields.Char("Program Start Time(HH:mm)", help="HH:mm")
    program_end_time = fields.Char("Program End Time (HH:mm)", help="HH:mm")
    program_budget = fields.Char("Program Budget")
    # program_collaborative_organization = fields.Many2many('collaborative.org.master',string="Collaborative Organization")
    program_collaborative_organization = fields.Char(string="Collaborative Organization")


    page_ref = fields.Many2one("organization.information")
