from odoo import models, api, fields
from datetime import datetime
import nepali_datetime


class ToleBikashMeetingDetails(models.Model):
    _name = "tole.bikash.meeting.details"
    _description = "Meeting Details"

    meeting_number = fields.Integer(
        string="Sabha/Bhela No.", help=" Sabha/Bhela Program"
    )

    meeting_date_bs = fields.Char(
        string=" Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )

    # For Generating Report
    meeting_year = fields.Char(store=True)
    meeting_month = fields.Char(store=True)
    meeting_day = fields.Char(store=True)
    week = fields.Char("Week", compute="_get_registration_day", store=True)
    meeting_time = fields.Char(" Time(HH:mm)", help="HH:mm")
    meeting_chairman_fullname = fields.Char(string="Chairman name")
    total_attendees = fields.Integer("Attendees Number")

    meeting_page_ref = fields.Many2one("tole.bikash.info")

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date

    @api.depends("meeting_date_bs")
    def _get_registration_day(self):
        for record in self:
            try:
                year, month, day = map(int, record.meeting_date_bs.split("-"))
                week_day = nepali_datetime.date(year, month, day).strftime("%G")
                record.week = week_day
                # For Report
                record.meeting_year = year
                record.meeting_month = month
                record.meeting_day = day
            except ValueError as e:
                # Handle the case when the string is not a valid date
                print(
                    f"Error: {e}. Invalid date format for registration_date_bs: {record.meeting_date_bs}"
                )
