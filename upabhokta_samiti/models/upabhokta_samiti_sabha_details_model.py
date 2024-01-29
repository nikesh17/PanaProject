from odoo import models, api, fields
from datetime import datetime
import nepali_datetime


class UpabhoktaSamitiSabhaDetails(models.Model):
    _name = "upabhokta.samiti.sabha.details"

    sabha_number = fields.Integer(
        string="Nth Sabha/Nagar Program", help="Nth Sabha/Nagar Program"
    )

    sabha_date_bs = fields.Char(
        string="Sabha Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )

    # For Generating Report
    sabha_year = fields.Char(store=True)
    sabha_month = fields.Char(store=True)
    sabha_day = fields.Char(store=True)
    week = fields.Char("Week", compute="_get_registration_day", store=True)
    sabha_time = fields.Char("Sabha Time(HH:mm)", help="HH:mm")
    sabha_chairman_fullname = fields.Char(string="Chairman")
    palika_representative_designation = fields.Many2one(
        "organization.designation.representative", string="Designation"
    )
    palika_representative_name = fields.Char("Palika Representative Name")
    chief_guest = fields.Char(string="Chief Guest")
    total_attendees = fields.Integer("Attendees Number")

    samiti_sabha_details_reference_page_id = fields.Many2one("upabhokta.samiti.info")

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date

    @api.depends("sabha_date_bs")
    def _get_registration_day(self):
        for record in self:
            try:
                year, month, day = map(int, record.sabha_date_bs.split("-"))
                week_day = nepali_datetime.date(year, month, day).strftime("%G")
                record.week = week_day
                # For Report
                record.sabha_year = year
                record.sabha_month = month
                record.sabha_day = day
            except ValueError as e:
                # Handle the case when the string is not a valid date
                print(
                    f"Error: {e}. Invalid date format for registration_date_bs: {record.sabha_date_bs}"
                )
