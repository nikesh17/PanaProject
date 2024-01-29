from odoo import fields, api, models

class ToleBikashAttendees(models.Model):
    _name = "tole.bikash.attendees"
    _description = "Tole BikashAttendees Details"
    
    genders_list = [("male", "Male"), ("female", "Female"), ("others", "Others")]
    
    full_name = fields.Char("Full Name")
    gender = fields.Selection(
        genders_list,
        string="Gender",
    )
    signature = fields.Binary(string="Signature", attachment=True)
    mobile = fields.Char("Mobile Number")
    email = fields.Char("Email")
    remarks = fields.Text(string="Remarks")
    attendee_id = fields.Many2one('tole.bikash.info')
    
 