from odoo import api, fields, models
import nepali_datetime


class UpabhoktaSamitiFormationMembers(models.Model):
    _name = "upabhokta.samiti.formation.members"
    _description = "Upabhokta Samiti Formation Members model"
    _rec_name = "member_full_name"

    user_id=fields.Char("UserId")
    member_designation_list = [
        ("chairperson_president", "Chairperson/President"),
        ("vice_chairperson_vice_president", "Vice Chairperson/Vice President"),
        ("secretary", "Secretary"),
        ("treasurer", "Treasurer"),
        ("member", "Member"),
        ("advisor_consultant", "Advisors/Consultants"),
        ("spokesperson", "Spokesperson"),
    ]
    gender_list = [("Male", "Male"), ("Female", "Female"), ("others", "Others")]
    member_full_name = fields.Char(string="Full Name", required=True)
    samiti_member_designation = fields.Many2one("organization.designation.organization")
    member_gender = fields.Selection(gender_list, string="Gender", required=True)
    member_address = fields.Char(string="Address", required=True)
    member_father_name = fields.Char(string="Father Name", required=True)
    member_grandfather_name = fields.Char(string="Grandfather Name", required=True)
    member_mobile = fields.Char(string="Mobile", required=True)
    member_telephone_opt = fields.Char(string="Telephone")
    member_citizenship_number = fields.Char(string="Citizenship Number")
    member_citizenship_issued_district = fields.Many2one(
        "location.district", string="Citizenship Issued District"
    )
    member_citizenship_issued_date_bs = fields.Char(
        string="Issued Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )
    member_signature=fields.Binary(string="Signature", attachment=True)
    member_picture=fields.Binary("PP Sized Picture", attachment=True)
    remarks = fields.Html()

    # page reference‰
    samiti_formation_members_reference_page_id = fields.Many2one(
        "upabhokta.samiti.info"
    )

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date
