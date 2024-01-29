from odoo import api, fields, models
import nepali_datetime


class OrganizationFormationMembers(models.Model):
    _name = "organization.formation.members"
    _description = "Organization Formation Members"
    _rec_name = "member_full_name"

    user_id = fields.Char("User ID")
    gender_list = [("Male", "Male"), ("Female", "Female"), ("others", "Others")]
    qualification_list = [
        ("school_level", "School Level"),
        ("Intermediate", "Intermediate"),
        ("Bachelor Degree", "Bachelor Degree"),
    ]

    member_full_name = fields.Char(string="Full Name", required=True)
    member_gender = fields.Selection(gender_list, string="Gender", required=True)
    organization_member_designation = fields.Many2one("org.representative.designation", string="Designation")
    member_address = fields.Char(string="Address", required=True)
    member_father_name = fields.Char(string="Father Name", required=True)
    member_mother_name = fields.Char(string="Mother Name", required=True)
    member_grandfather_name = fields.Char(string="Grandfather Name", required=True)
    member_mobile = fields.Char(string="Mobile", required=True)
    member_email = fields.Char(string="Email", required=True)
    qualification_level_ = fields.Many2one('member.qualification.master', string="Qualification")

    member_telephone_opt = fields.Char(string="Telephone")
    member_citizenship_number = fields.Char(string="Citizenship Number")
    member_citizenship_issued_district = fields.Many2one(
        "location.district", string="Citizenship Issued District"
    )
    member_citizenship_issued_date_bs = fields.Char(
        string="Issued Date (BS)", default=lambda self: self._set_default_bs_date_today()
    )
    citizenship_front_image = fields.Binary(string="Citizenship Front Image", attachment=True)
    citizenship_back_image = fields.Binary(string="Citizenship Back Image", attachment=True)

    member_signature = fields.Binary(string="Signature", attachment=True)
    member_picture = fields.Binary(string="PP Sized Picture", attachment=True)
    
    comitte_member_tenure = fields.Many2one( 'fiscal.year',string="Tenure Duration")
    member_type = fields.Many2one( 'quota.master',string="Quota")
    status = fields.Boolean("Member Status")

    # Page reference
    organization_formation_members_reference_page_id = fields.Many2one(
        "organization.information"
    )

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date
