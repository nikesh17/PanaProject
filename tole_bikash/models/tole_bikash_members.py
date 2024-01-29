from odoo import fields, models, api
import nepali_datetime
import csv
from io import StringIO
import base64

class ToleBikashMember(models.Model):
    _name = "tole.bikash.member"
    _description = "Tole Bikash Member"
    _rec_name = "member_name"


    gender_list = [("Male", "Male"), ("Female", "Female"), ("others", "Others")]

    member_name = fields.Char("Full Name")
    member_gender = fields.Selection(gender_list, string="Gender")
    member_designation = fields.Many2one("organization.designation.organization", string="Designation")
    member_location = fields.Char("Location")
    member_phone = fields.Char("Phone")
    member_email = fields.Char("Email")
    qualification_level = fields.Many2one('member.qualification.master', string="Qualification")

    member_citizenship_number = fields.Char(string="Citizenship Number")
    member_citizenship_issued_district = fields.Many2one(
        "location.district", string="Citizenship Issued District"
    )
    member_citizenship_issued_date_bs = fields.Char(
        string="Issued Date (BS)", default=lambda self: self._set_default_bs_date_today()
    )
    citizenship_front_back = fields.Many2many('ir.attachment',string="Citizenship Image", attachment=True)

    member_family_male = fields.Integer("Male")
    member_family_female = fields.Integer("Female")
    member_family_total = fields.Integer(string="Total", compute='_compute_member_family_total', store=True)

    member_signature = fields.Binary("Signture", attachment=True)
    member_picture = fields.Binary(string="PP Sized Picture", attachment=True)

    member_id = fields.Many2one('tole.bikash.info')

    csv_file = fields.Binary(string='CSV File', attachment=True, help='Upload CSV file')

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date
    
    @api.depends('member_family_male', 'member_family_female')
    def _compute_member_family_total(self):
        for record in self:
            record.member_family_total = record.member_family_male + record.member_family_female

    def import_csv(self):
        if self.csv_file:
            # Decode the binary data and create a CSV reader
            csv_data = base64.b64decode(self.csv_file)
            csv_text = csv_data.decode('utf-8')
            csv_reader = csv.DictReader(StringIO(csv_text))

            for row in csv_reader:
                # Create a new record for each row in the CSV
                tole_bikash_member_data = {
                    'member_name': row.get('member_name'),
                    'member_phone': row.get('member_phone'),
                    'member_email': row.get('member_email'),
                    # Add other fields as needed
                }
                self.create(tole_bikash_member_data)
                

            return "CSV file imported successfully."
        else:
            return "No CSV file uploaded."