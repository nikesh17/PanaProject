from odoo import api, models, fields


class AttendeesModel(models.Model):
    _name = "upabhokta.samiti.attendees"
    _description = "Attendees Details"
    
    genders_list = [("male", "Male"), ("female", "Female"), ("others", "Others")]
    
    full_name = fields.Char("Full Name")
    gender = fields.Selection(
        genders_list,
        string="Gender",
    )
    signature = fields.Binary(string="Signature", attachment=True)
    mobile = fields.Char("Mobile Number")
    remarks = fields.Text(string="Remarks")
    attendees_id = fields.Many2one("upabhokta.samiti.info")
    
 
    