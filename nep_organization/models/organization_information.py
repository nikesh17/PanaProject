from odoo import api, models, fields
import nepali_datetime
from datetime import datetime

class OrganzationInfo(models.Model):
    _name = "organization.information"
    _description = "Organization Basic Details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    org_name_en = fields.Char("Organization Name(English)", required=True, tracking=True)
    org_name_np = fields.Char("Organization Name(Nepali)")
    org_shortcut_name = fields.Char("Organization Shortcut Name" , required=True, tracking=True)
    org_category = fields.Many2one("upabhokta.samiti.category" , tracking=True)
    org_province = fields.Many2one("location.province", string="Province")
    org_district = fields.Many2one("location.district", string="District")
    org_municipality = fields.Many2one("location.palika", string="Palika")
    org_ward = fields.Integer("Ward")
    org_tole = fields.Char("Tole")
    org_email = fields.Char("Email")
    org_telephone = fields.Char("Telephone")
    org_postbox_number = fields.Char("Post Box Number")
    org_fax_number = fields.Char("Fax Number")
    org_house_number = fields.Char("House Number")
    org_website_url = fields.Char("Website URL")
    contact_person_name_ = fields.Char(
        "Name",
    )
    contact_person_phone_ = fields.Char(" Phone")
    contact_person_email_ = fields.Char(" Email")
    contact_person_designation = fields.Many2one("organization.designation.organization")
    comments = fields.Html()
    organization_type = fields.Many2one(
        "organization.type",
        string="Organization Type",
        
       
    )
    organization_logo = fields.Binary(string="Upload Logo")
    
    election_date=fields.Char("Election Date")
    committee_member_tenure=fields.Many2one("fiscal.year")
    
     # Date in NP
    registration_date_bs = fields.Char(
        string="Registration Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )
    # For Generating Report
    current_year = fields.Char(store=True)
    current_month = fields.Char(store=True)
    current_day = fields.Char(store=True)

    # reference to bhela details
    organization_bhela_details = fields.One2many(
        "organization.sabha.details",
        "sanstha_details_reference_page_id",
        "Bhela details",
    )
    # reference to purpose
    organization_purpose = fields.One2many(
        "organization.purpose",
        "page_ref",
        "Organization Purpose",
    )
    # Reference to formation memeber
    organization_members_ref = fields.One2many(
        "organization.formation.members",
        "organization_formation_members_reference_page_id",
        string="Organization Members",
    ) 
     # Reference to attendees page 
    attendees = fields.One2many(
        "organization.attendees", "attendees_id", string="Attendees"
    )
     # Reference to fix assets
    fix_assets_ref = fields.One2many(
        "organization.fix.assets", "asset_ref_id", string="Fix Assets"
    )
     # reference to renewal
    organization_renewal_ref = fields.One2many(
        "organization.renewal",
        "renewal_page_ref",
        "Organization Renewal Detail",
    )
    # Benificiary reference
    beneficiary_ref = fields.One2many(
        "organization.beneficiary.record",
        "page_ref",
        string="Beneficiary Record",
    )
    # program reference
    program_ref = fields.One2many(
        "organization.program.record",
        "page_ref",
        string="Program Record",
    )
    quota_ref = fields.One2many(
        "organization.member.quota",
        "page_ref",
        string="Quota",
    )
    
    
    # For Ribbon and status
    organization_status = fields.Selection(
        [
            ("in_review", "In Review"),
            ("incomplete_submitted", "Incomplete Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="in_review",
    )
    
    # Buttons
    
    def set_state_in_review(self):
       
        for record in self:
            record.organization_status = "in_review"

    def set_state_incomplete_submitted(self):
       
        for record in self:
            record.organization_status = "incomplete_submitted"
            record.contact_customer_incomplete()


    def set_state_verified(self):
         for record in self:
            record.organization_status = "approved"
            record.contact_customer_verification()

    
    def set_state_rejected(self):
        for record in self:
            record.organization_status = "rejected"
            record.contact_customer_rejection()

            
    
    # Email Generation
    # def contact_customer_verification(self):
       
        # template_ref = self.env.ref(
        #     "organization_module.organization_email_template_verified"
        # )
         # Render the QWeb report and attach it to the email
        # report = self.env['ir.actions.report']._get_report_from_name('organization_module.organization_pramad_patra')
        # pdf_content, format = report.with_context().sudo().render([self.id])

        # # Attach the PDF to the email
        # template_ref.attachment_ids = [(0, 6, {
        #     'name': 'organization_report.pdf',
        #     'datas': pdf_content,
        #     'mimetype': 'application/pdf',
        # })]

        # return template_ref.send_mail(self.id, force_send=True)


        # return template_ref.send_mail(self.id, force_send=True)

    # def contact_customer_rejection(self):
        # template_ref = self.env.ref(
        #     "organization_module.organization_email_template_rejected"
        # )
        # return template_ref.send_mail(self.id, force_send=True)

    # def contact_customer_incomplete(self):
        # template_ref = self.env.ref(
        #     "organization_module.organization_email_template_incomplete"
        # )
        # return template_ref.send_mail(self.id, force_send=True)

     
    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date

    @api.depends("registration_date_bs")
    def _get_registration_day(self):
        for record in self:
            try:
                year, month, day = map(int, record.registration_date_bs.split("-"))
                # For Report
                record.current_year = year
                record.current_month = month
                record.current_day = day
            except ValueError as e:
                # Handle the case when the string is not a valid date
                print(
                    f"Error: {e}. Invalid date format for registration_date_bs: {record.current_date_bs}"
                )

     
    # Email Generation
    def contact_customer_verification(self):
       
        template_ref = self.env.ref(
            "nep_organization.organization_email_template_verified"
        )
        
        return template_ref.send_mail(self.id, force_send=True)

    def contact_customer_rejection(self):
        template_ref = self.env.ref(
            "nep_organization.organization_email_template_rejected"
        )
        return template_ref.send_mail(self.id, force_send=True)

    def contact_customer_incomplete(self):
        template_ref = self.env.ref(
            "nep_organization.organization_email_template_incomplete"
        )
        return template_ref.send_mail(self.id, force_send=True)
