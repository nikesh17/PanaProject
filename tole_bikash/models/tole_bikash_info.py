from odoo import fields, models, api
import nepali_datetime

class ToleBikashInfo(models.Model):
    _name = "tole.bikash.info"
    _description =  "Tole bikash info"
    _rec_name = "tole_bikash_name_en"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    tole_bikash_name_en = fields.Char(" Name(English)", tracking=True, required=True)
    tole_bikash_name_np = fields.Char(" Name(Nepali)",  required=True)
    Tole_bikash_category = fields.Many2one("upabhokta.samiti.category" , tracking=True, string="Category")
    tole_bikash_type = fields.Many2one(
        "organization.type",
        string=" Type",
        
       
    )
    tole_bikash_logo = fields.Binary(string="Upload Logo")

    tole_bikash_email = fields.Char("Email")
    tole_bikash_telephone = fields.Char("Telephone")
    tole_bikash_postbox_number = fields.Char("Post Box Number")
    tole_bikash_fax_number = fields.Char("Fax Number")
    
    
    #location
    province = fields.Many2one("location.province", string="Province")
    district = fields.Many2one("location.district", string="District")
    municipality = fields.Many2one("location.palika", string="Municipality" )
    ward = fields.Integer("Ward")
    tole = fields.Char("Tole")

    #border
    east = fields.Integer("East")
    west = fields.Integer("West")
    north = fields.Integer("North")
    south = fields.Integer("South")

    #contact
    contact_person_name = fields.Char("Name")
    contact_person_phone = fields.Char("Phone")
    contact_person_email = fields.Char("Email")
    contact_person_location = fields.Char("Location")
    contact_person_designation = fields.Many2one("organization.designation.organization", string="Designation")

    #date
    registration_date_bs = fields.Char(string="Registration Date(BS)",
        default=lambda self: self._set_default_bs_date_today(),
    )
    
    # Comment
    comments = fields.Html("Comment")
    
    decisions = fields.One2many('tole.bikash.decision', 'decision_id', string="Decisions")
    proposals = fields.One2many('tole.bikash.proposal', 'proposal_id', string="Proposals")
    members = fields.One2many('tole.bikash.member', 'member_id', string="Members")
    attendees = fields.One2many('tole.bikash.attendees', 'attendee_id', string="Attendees")
    meetings = fields.One2many('tole.bikash.meeting.details', 'meeting_page_ref', string="Meetings")

    #For Ribbon and Status
    tole_bikash_status = fields.Selection(
        [
            ("in_review","In Review"),
            ("incomplete_submitted","Incomplete Submitted"),
            ("approved","Approved"),
            ("rejected","Rejected"),
        ],
        default="in_review"
    )

    def _set_default_bs_date_today(self):
        today_date = nepali_datetime.date.today()
        return today_date



 # Buttons
    
    def set_state_in_review(self):
        notification_records = (
            self.env["tole.bikash.notification"]
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
            record.tole_bikash_status = "in_review"
            

    def set_state_incomplete_submitted(self):
        notification_records = (
            self.env["tole.bikash.notification"]
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
            record.tole_bikash_status = "incomplete_submitted"
            record.contact_customer_incomplete()


    def set_state_verified(self):
        notification_records = (
            self.env["tole.bikash.notification"]
            .sudo()
            .create(
                {
                    "message": self.comments,
                    "sent_by": self.env.user.id,
                    "sent_to": self.create_uid.id,
                }
            )
        )
        # Registration number
        district_code = self.district.id
        sequence_number= self.env['ir.sequence'].next_by_code('tole.bikash.registration.sequence')

        date = nepali_datetime.date.today()
        year = date.year
        month = date.month

        reg_year = int(year)%100
        if (month>=4):
            fiscal_year = f"{reg_year}/{reg_year+1}"
        else:
            fiscal_year = f"{reg_year-1}/{reg_year}"
            
        reg_number = f"{fiscal_year}-{district_code}-{sequence_number}"
        tole_bikash_master = self.env["tole.bikash.master"].sudo().search([])
        response =tole_bikash_master.sudo().create({
            "user_id" : self.env.user.id,
            "info_id" :  self.id,
            "meeting_id" : self.meetings.create_uid.id,
            "member_formation_id" : self.members.create_uid.id,
            "proposal_id" : self.proposals.create_uid.id,
            "decision_id" : self.decisions.create_uid.id,
            "attendees_create_uid" : self.attendees.create_uid.id, 
            "registration_number" : reg_number
            
        })

        
        for record in self:
            record.tole_bikash_status = "approved"
            record.contact_customer_verification()

    
    def set_state_rejected(self):
        notification_records = (
            self.env["tole.bikash.notification"]
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
            record.tole_bikash_status = "rejected"
            record.contact_customer_rejection()

# Email Generation
    def contact_customer_verification(self):
       
        template_ref = self.env.ref(
            "tole_bikash.class_d_organization_email_template_verified"
        )
        
        return template_ref.send_mail(self.id, force_send=True)

    def contact_customer_rejection(self):
        template_ref = self.env.ref(
            "tole_bikash.class_d_organization_email_template_rejected"
        )
        return template_ref.send_mail(self.id, force_send=True)

    def contact_customer_incomplete(self):
        template_ref = self.env.ref(
            "tole_bikash.class_d_organization_email_template_incomplete"
        )
        return template_ref.send_mail(self.id, force_send=True)
    
    def get_registration_number(self):
            tole_bikash_master = self.env["tole.bikash.master"].sudo().search([("info_id", "=", self.id)], limit=1)
            return tole_bikash_master.registration_number
