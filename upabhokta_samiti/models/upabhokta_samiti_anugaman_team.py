from odoo import api, fields, models


class AnugamanTeam(models.Model):
    _name = "upabhokta.samiti.anugaman.team"
    _description = "Upabhokta Samiti Anugaman Team Model"
    _rec_name = "full_name"

    gender_list = [("Male", "Male"), ("Female", "Female"), ("others", "Others")]

    anugaman_member_designation = fields.Many2one("organization.designation.organization")
    full_name = fields.Many2one("upabhokta.samiti.formation.members")
    member_gender = fields.Selection(gender_list, string="Gender", required=True)
    member_address = fields.Char(string="Address", required=True)
    member_mobile = fields.Char(string="Mobile", required=True)
    member_telephone_opt = fields.Char(string="Telephone")
    member_citizenship_number = fields.Char(string="Citizenship Number")
    member_citizenship_issued_district = fields.Many2one(
        "location.district", string="Citizenship Issued District"
    )
    member_citizenship_issued_date_bs = fields.Char(
        string="Issued Date(BS)",
    )
    # Notebook reference
    notebook_reference_id = fields.Many2one("upabhokta.samiti.info")
