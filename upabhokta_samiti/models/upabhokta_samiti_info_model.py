from odoo import api, fields, models
import datetime
import nepali_datetime


class UpabhoktaSamitiInfo(models.Model):
    _name = "upabhokta.samiti.info"
    _description = "Upabhokta Samiti Info Model"
    _rec_name = "upabhokta_samiti_name"
    _inherit = "mail.thread"

    upabhokta_samiti_name = fields.Char(
        string="Upabhokta Samiti Name", required=True, tracking=True
    )

    """
    return the id for Upabhokta Samiti
    """
    user_id = fields.Char("UerID")
    upabhokta_samiti_type = fields.Many2one(
        "organization.type",
        string="Organization Type",
        default=lambda self: self._set_default_organization_type(),
        readonly=True,
        store=True,
    )

    upabhokta_samiti_category = fields.Many2one("upabhokta.samiti.category")

    contact_person_name_ = fields.Char(
        "Name",
    )
    contact_person_phone_ = fields.Char("Phone")
    contact_person_email_ = fields.Char("Email")

    sabha_number = fields.Integer(
        string="Nth Sabha/Nagar Program", help="Nth Sabha/Nagar Program"
    )
    # Date in NP
    registration_date_bs = fields.Char(
        string="Registration Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )
    # For Generating Report
    sabha_year = fields.Char(store=True)
    sabha_month = fields.Char(store=True)
    sabha_day = fields.Char(store=True)

    sabha_time = fields.Char("Sabha Time(HH:mm)", help="HH:mm")
    sabha_chairman_fullname = fields.Char(string="Chairman")
    week = fields.Char("Week", compute="_get_registration_day", store=True)
    palika_representative_designation = fields.Many2one(
        "organization.designation.representative", string="Designation"
    )
    palika_representative_name = fields.Char("Name")
    province = fields.Many2one("location.province")
    district = fields.Many2one("location.district")
    municipality = fields.Many2one("location.palika")
    ward = fields.Integer("Ward")
    tole = fields.Char("Tole")
    # Yojana Details
    yojana_name = fields.Char("Yojana Name")
    yojana_type = fields.Many2one("org.yojana.type", string="Yojana Type")
    yojana_budget_npr = fields.Float(string="Yojana Budget(NPR)", default=0)
    yojana_budget_type = fields.Many2one("org.budget.type", string="Budget Type")
    bank_details = fields.Many2one("upabhokta.samiti.bank.account")

    # For PDF
    upabhokta_samiti_members = fields.Many2one("upabhokta.samiti.formation.members")

    # Other Details
    chief_guest = fields.Char(string="Chief Guest")
    total_attendees = fields.Integer("Attendees Number")
    # project_proposal = fields.Html(string="Project proposal")
    upabhokta_samiti_status = fields.Selection(
        [
            ("in_review", "In Review"),
            ("incomplete_submitted", "Incomplete Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="in_review",
    )

    upabhokta_samiti_logo = fields.Binary(string="Upload Logo")
    comments = fields.Html()

    # Reference to attendees page to Upabhokta Samiti
    attendees = fields.One2many(
        "upabhokta.samiti.attendees", "attendees_id", string="Attendees"
    )
    # Reference to beneficiary page to Upabhokta Samiti
    beneficiary_ref = fields.One2many(
        "upabhokta.samiti.beneficiary.record",
        "page_ref",
        string="Beneficiary Record",
    )

    project_proposal_page = fields.One2many(
        "upabhokta.samiti.project.proposal",
        "page_ref",
        "Project Proposal",
    )
    # samiti members reference
    upabhokta_samiti_members_ref = fields.One2many(
        "upabhokta.samiti.formation.members",
        "samiti_formation_members_reference_page_id",
        string="Samiti Members",
    )
    # reference to sabha details
    upabhokta_samiti_sabha_details_ref = fields.One2many(
        "upabhokta.samiti.sabha.details",
        "samiti_sabha_details_reference_page_id",
        string="Sabha Details",
    )

    # Anugaman Team Reference
    anugaman_teamref_id = fields.One2many(
        "upabhokta.samiti.anugaman.team",
        "notebook_reference_id",
    )

    # Bank details
    bank_details_ref = fields.One2many(
        "upabhokta.samiti.bank.account", "bank_details_id"
    )
    # Bank details
    bank_details_request_ref = fields.One2many(
        "upabhokta.samiti.project.bankreq", "page_ref"
    )

    # Function to set default value for Many2one Uapabhokta Samiti Type
    def _set_default_organization_type(self, **type):
        upabhokta_samiti = (
            self.env["organization.type"]
            .sudo()
            .search([("type", "=", "Upabhokta Samiti")], limit=1)
        )
        return upabhokta_samiti.id if upabhokta_samiti else False

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date

    @api.depends("registration_date_bs")
    def _get_registration_day(self):
        for record in self:
            try:
                year, month, day = map(int, record.registration_date_bs.split("-"))
                week_day = nepali_datetime.date(year, month, day).strftime("%G")
                record.week = week_day
                # For Report
                record.sabha_year = year
                record.sabha_month = month
                record.sabha_day = day
            except ValueError as e:
                # Handle the case when the string is not a valid date
                print(
                    f"Error: {e}. Invalid date format for registration_date_bs: {record.registration_date_bs}"
                )

    def set_state_in_review(self):
        notification_records = (
            self.env["upabhokta.samiti.notification"]
            .sudo()
            .create(
                {
                    "message": "Your form is successfully submitted.",
                    "sent_by": self.env.user.id,
                    "sent_to": self.create_uid.id,
                }
            )
        )
        for record in self:
            record.upabhokta_samiti_status = "in_review"

    def set_state_incomplete_submitted(self):
        notification_records = (
            self.env["upabhokta.samiti.notification"]
            .sudo()
            .create(
                {
                    "message": self.comments,
                    "sent_by": self.env.user.id,
                    "sent_to": self.create_uid.id,
                }
            )
        )
        for record in self:
            record.upabhokta_samiti_status = "incomplete_submitted"

    def set_state_verified(self):
        # notification
        notification_records = (
            self.env["upabhokta.samiti.notification"]
            .sudo()
            .create(
                {
                    "message": "Your form is approved.",
                    "sent_by": self.env.user.id,
                    "sent_to": self.create_uid.id,
                }
            )
        )

        # Registration number
        district_code = self.district.id
        sequence_number= self.env['ir.sequence'].next_by_code('upabhokta.samiti.registration.sequence')

        date = nepali_datetime.date.today()
        year = date.year
        month = date.month

        reg_year = int(year)%100
        if (month>=4):
            fiscal_year = f"{reg_year}/{reg_year+1}"
        else:
            fiscal_year = f"{reg_year-1}/{reg_year}"
            
        reg_number = f"{fiscal_year}-{district_code}-{sequence_number}"

        upabhokta_samiti_master = self.env["upabhokta.samiti.master"].sudo().search([])

        response = upabhokta_samiti_master.sudo().create(
            {
                "user_id": self.env.user.id,
                "info_id": self.id,
                "bhela_id": self.upabhokta_samiti_sabha_details_ref.id,
                "formation_member_create_uid": self.upabhokta_samiti_members_ref.create_uid.id,
                "beneficiary_create_uid": self.beneficiary_ref.create_uid.id,
                "proposal_id": self.project_proposal_page.id,
                "attendees_create_uid": self.attendees.create_uid.id,
                "bank_account_create_uid": self.bank_details_ref.create_uid.id,
                "bank_request_create_uid": self.bank_details_request_ref.create_uid.id,
                "anugaman_create_uid": self.anugaman_teamref_id.create_uid.id,
                "registration_number": reg_number,
            }
        )

        for record in self:
            record.upabhokta_samiti_status = "approved"
            self.upabhokta_samiti_verified_email()


    def set_state_rejected(self):
        notification_records = (
            self.env["upabhokta.samiti.notification"]
            .sudo()
            .create(
                {
                    "message": self.comments,
                    "sent_by": self.env.user.id,
                    "sent_to": self.create_uid.id,
                }
            )
        )

        for record in self:
            record.upabhokta_samiti_status = "rejected"

    # Report Generation
    def _get_report_base_filename(self):
        return self.upabhokta_samiti_name

    # Email Generation
    def upabhokta_samiti_verified_email(self):
        template_ref = self.env.ref(
            "upabhokta_samiti.upbhokta_samiti_email_template_verified_"
        )
        return template_ref.send_mail(self.id, force_send=True)
