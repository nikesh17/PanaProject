from odoo import http
from odoo.http import request
import base64


class ToleBikashController(http.Controller):
    @http.route("/tole-bikash/dashboard", type="http", website=True, auth="user")
    def tolbikash_dashboard_page(self):
        # Information of Tole Bikash
        tole_bikash_info = (
            request.env["tole.bikash.info"]
            .sudo()
            .search([("create_uid", "=", request.env.user.id)], limit=1)
        )
        
        # Notification
        notifications = (
            request.env["tole.bikash.notification"]
            .sudo()
            .search([
                ("sent_to", "=", request.env.user.id),
                ("status", "=", False),
            ], order="sent_at desc")
        )
        
        return request.render(
            "tole_bikash.tole_bikash_dashboard_template",
            {
                "tole_bikash_info": tole_bikash_info,
                "notifications": notifications,
            },
        )

# GET | POST : /tole-bikash/basic-details
    @http.route("/tole-bikash/basic-details", type="http", website=True, auth="user")
    def tol_bikash_basic_details(self, **data):
        districts = http.request.env["location.district"].sudo().search([])
        provinces = http.request.env["location.province"].sudo().search([])
        palika = http.request.env["location.palika"].sudo().search([])
        org_designations = (
            http.request.env["organization.designation.organization"]
            .sudo()
            .search([])
        )
        fiscal_year = http.request.env["fiscal.year"].sudo().search([])
        organization_type = http.request.env["organization.type"].sudo().search([])

        check_if_tole_bikash_exists = (
            http.request.env["tole.bikash.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )

        org_external_details = {
            "districts": districts,
            "provinces": provinces,
            "palika": palika,
            "organization_type": organization_type,
            "contact_person_name": http.request.env.user.partner_id.name,
            "contact_person_phone": http.request.env.user.phone,
            "contact_person_email": http.request.env.user.email,
            "contact_person_designation": org_designations,
            "fiscal_year": fiscal_year,
        }

        if http.request.httprequest.method == "POST":
            tole_bikash_logo_raw = data.get("tole_bikash_logo").read()
            organization_logo_binary = base64.b64encode(tole_bikash_logo_raw)

            inserted_data = {
                "tole_bikash_name_en": data.get("tole_bikash_name_en"),
                "tole_bikash_name_np": data.get("tole_bikash_name_np"),
                "Tole_bikash_category": data.get("Tole_bikash_category"),
                "tole_bikash_type": data.get("tole_bikash_type"),
                "tole_bikash_email": data.get("tole_bikash_email"),
                "tole_bikash_telephone": data.get("tole_bikash_telephone"),
                "tole_bikash_postbox_number": data.get("tole_bikash_postbox_number"),
                "tole_bikash_fax_number": data.get("tole_bikash_fax_number"),
                "province": data.get("province"),
                "district": data.get("district"),
                "municipality": data.get("municipality"),
                "ward": data.get("ward"),
                "tole": data.get("tole"),
                "east": data.get("east"),
                "west": data.get("west"),
                "north": data.get("north"),
                "south": data.get("south"),
                "contact_person_name": data.get("contact_person_name"),
                "contact_person_phone": data.get("contact_person_phone"),
                "contact_person_email": data.get("contact_person_email"),
                "contact_person_designation": data.get("contact_person_designation"),
                "tole_bikash_logo": organization_logo_binary,
            }
            http.request.env["tole.bikash.info"].sudo().create(inserted_data)
            return http.request.redirect("/tole-bikash/basic-details")

        return http.request.render(
            "tole_bikash.tole_bikash_basic_details_template", {
                "org_external_details": org_external_details,
                "check_if_tole_bikash_exists": check_if_tole_bikash_exists,
            }
        )
        
# GET|POST Bhela Details: /tole-bikash/meeting-details
    @http.route(
        ["/tole-bikash/meeting-details"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def tol_bikash_meeting_details(self, **data):
        sabha_details = (
            request.env["tole.bikash.meeting.details"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )

        if request.httprequest.method == "POST":
            meeting_number = data.get("meeting_number")
            meeting_date_bs = data.get("meeting_date_bs")
            meeting_time = data.get("meeting_time")
            meeting_chairman_fullname = data.get("meeting_chairman_fullname")
            total_attendees = data.get("total_attendees")
            _page = (
                request.env["tole.bikash.info"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
            page = _page.id

            sabha_record = {
                "meeting_number": meeting_number,
                "meeting_date_bs": meeting_date_bs,
                "meeting_time": meeting_time,
                "meeting_chairman_fullname": meeting_chairman_fullname,
                "total_attendees": total_attendees,
                "meeting_page_ref": page,
            }

            request.env["tole.bikash.meeting.details"].sudo().create(sabha_record)
            return print("Data received.")

        return request.render(
            "tole_bikash.tole_bikash_meeting_details_template",
            {
                "sabha_details": sabha_details,
            },
        )
   
   
# GET | POST  Tole Bikash Purpose

    @http.route(
        ["/tole-bikash/proposal"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def tole_bikash_proposal(self, **data):
        document = (
            request.env["tole.bikash.proposal"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        if request.httprequest.method == "POST":
            proposal_detail = data.get("editor")
            proposal_document = data.get("proposal_document")
            signed_document_data = proposal_document.read()
            proposal_name = proposal_document.filename
            _page = (
                request.env["tole.bikash.info"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
            page = _page.id
            response = (
                request.env["tole.bikash.proposal"]
                .sudo()
                .create(
                    {
                        "proposal_detail": proposal_detail,
                        "proposal_document": base64.b64encode(signed_document_data),
                        "proposal_name": proposal_name,
                        "proposal_id": page,
                    }
                )
            )
            if response:
                return request.redirect("/tole-bikash/purposes")
        return request.render("tole_bikash.tole_bikash_purpose_template", {'document': document})

# GET | POST  Tole Bikash Members /tole-bikash/member-details
    @http.route(
        ["/tole-bikash/member-details"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def tole_bikash_members(self, **form_data):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        tole_bikash_info = http.request.env["tole.bikash.info"].sudo().search([])
        qualification = request.env["member.qualification.master"].sudo().search([])

        members_detail = (
            request.env["tole.bikash.member"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )

        org_designations = (
            http.request.env["organization.designation.organization"].sudo().search([])
        )
        if request.httprequest.method == "POST":
            member_name = form_data.get("member_full_name")
            member_gender = form_data.get("member_gender")
            member_designation = form_data.get("org_designation")
            member_location = form_data.get("member_address")
            member_picture = form_data.get("profile")
            profile_file = member_picture.read()
            member_signature = form_data.get("signature")
            signature_file = member_signature.read()
            member_phone = form_data.get("mobile")
            member_email = form_data.get("email")
            member_citizenship_number = form_data.get("citizenship_number")
            member_citizenship_issued_district = form_data.get("issued_district")
            member_citizenship_issued_date_bs = form_data.get("issued_date_bs")
            qualification_level = form_data.get("qualification")
            member_family_male = form_data.get("member_family_male")
            member_family_female = form_data.get("member_family_female")
            member_family_total = form_data.get("member_family_total")
            citizenship_files = request.httprequest.files.getlist(
                "citizenship_front_back"
            )

            _page = (
                request.env["tole.bikash.info"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )

            page = _page.id

            new_member_record = (
                request.env["tole.bikash.member"]
                .sudo()
                .create(
                    {
                        "member_name": member_name,
                        "member_gender": member_gender,
                        "member_designation": member_designation,
                        "member_location": member_location,
                        "member_signature": base64.b64encode(signature_file),
                        "member_picture": base64.b64encode(profile_file),
                        "member_phone": member_phone,
                        "member_email": member_email,
                        "member_citizenship_number": member_citizenship_number,
                        "member_citizenship_issued_district": member_citizenship_issued_district,
                        "member_citizenship_issued_date_bs": member_citizenship_issued_date_bs,
                        "qualification_level": qualification_level,
                        "member_family_male": member_family_male,
                        "member_family_female": member_family_female,
                        "member_family_total": member_family_total,
                        "member_id": page,
                    }
                )
            )

            for file in citizenship_files:
                citizenship_file = file.read()
                new_attachment_record = (
                    request.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": file.filename,
                            "res_model": "tole.bikash.member",
                            "type": "binary",
                            "store_fname": file.filename,
                            "datas": base64.b64encode(citizenship_file),
                        }
                    )
                )
                new_member_record.write(
                    {"citizenship_front_back": [(4, new_attachment_record.id)]}
                )

            return request.redirect("/tole-bikash/member-details")

        return request.render(
            "tole_bikash.tole_bikash_members_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "tole_bikash_info": tole_bikash_info,
                "org_designations": org_designations,
                "members_detail": members_detail,
                "qualification": qualification,
            },
        )

# GET | POST Tole Bikash Attendees Details /tole-bikash/attendees
    @http.route(
        "/tole-bikash/attendees",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def attendees_details(self, **form_data):
        attendees_list = (
            request.env["tole.bikash.attendees"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        if request.httprequest.method == "POST":

            tole_bikash_attendees_name = form_data.get(
                "tole_bikash_attendees_name"
            )
            tole_bikash_attendees_gender = form_data.get(
                "tole_bikash_attendees_gender"
            )

        
            signature = form_data.get("signature")
            signature_file = signature.read()
            mobile = form_data.get("mobile")
            email = form_data.get("email")


            _page = (
                request.env["tole.bikash.info"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
            page = _page.id
            
            request.env["tole.bikash.attendees"].sudo().create(
                {
                    "full_name": tole_bikash_attendees_name,
                    "gender": tole_bikash_attendees_gender,
                    "mobile": mobile,
                    "signature": base64.b64encode(signature_file),
                    "email": email,
                    "attendee_id": page,
                }
            )
            return request.redirect("/tole-bikash/attendees")
        
        return request.render(
            "tole_bikash.tole_bikash_attendees_details_template",
            {"attendees_list": attendees_list},
        )
    
# GET | POST  Tole Bikash Decision /tole-bikash/decisions

    @http.route(
        ["/tole-bikash/decisions"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def tole_bikash_decisions(self, **data):
        document = (
            request.env["tole.bikash.decision"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        if request.httprequest.method == "POST":
            decision_detail = data.get("editor")
            decision_document = data.get("decision_document")
            signed_document_data = decision_document.read()
            decision_name = decision_document.filename
            _page = (
                request.env["tole.bikash.info"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
            page = _page.id
            response = (
                request.env["tole.bikash.proposal"]
                .sudo()
                .create(
                    {
                        "decision_detail": decision_detail,
                        "decision_document": base64.b64encode(signed_document_data),
                        "decision_name": decision_name,
                        "decision_id": page,
                    }
                )
            )
            if response:
                return request.redirect("/tole-bikash/decisions")
        return request.render("tole_bikash.tole_bikash_decision_template", {'document': document})

    @http.route("/error")
    def error_message(self):
        return request.render("tole_bikash.error_page")
    
    @http.route("/success")
    def success_message(self):
        return request.render("tole_bikash.success_page")


