from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.home import ensure_db
import json
import base64


class AuthSignupInheritHome(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        ensure_db()
        response = super(AuthSignupInheritHome, self).web_auth_signup(*args, **kw)

        upabhokta_samiti_categories = (
            request.env["upabhokta.samiti.category"].sudo().search([])
        )

        return request.render(
            "auth_signup.signup", {"categories": upabhokta_samiti_categories}
        )


class AuthSignupInheritValues(AuthSignupHome):
    @http.route("/web/signup", type="http", auth="public", website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        response = super(AuthSignupInheritValues, self).web_auth_signup(*args, **kw)
        user = (
            request.env["res.users"]
            .sudo()
            .search([("login", "=", qcontext.get("login"))])
        )
        if request.httprequest.method == "POST":
            upabhokta_samiti_category_str = kw.get("upabhokta_samiti_category")

            upabhokta_samiti_category_int = int(upabhokta_samiti_category_str)
            additional_fields = {
                "phone": kw.get("phone"),
                "upabhokta_samiti_category": upabhokta_samiti_category_int,
            }
            user.sudo().write(additional_fields)
            template = request.env.ref(
                "auth_signup.mail_template_user_signup_account_created",
                raise_if_not_found=False,
            )
            return self.web_login(*args, **kw)
        return response


class UpabhoktaSamitiController(http.Controller):
    # User Dashboard
    # GET: /upabhokta-samiti/dashboard
    @http.route("/upabhokta-samiti/dashboard", type="http", website=True, auth="user")
    def dashboar_page(self):
        upabhokta_samiti_info = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        # notification
        notifications = (
            request.env["upabhokta.samiti.notification"]
            .sudo()
            .search(
                [
                    ("sent_to", "=", http.request.env.user.id),
                    ("status", "=", False),
                ],
                order="sent_at desc",
            )
        )
        return request.render(
            "upabhokta_samiti.dashboard_template",
            {
                "upabhokta_samiti_info": upabhokta_samiti_info,
                "notifications": notifications,
            },
        )

    # Registration Page
    # GET: /upabhokta-samiti/register
    @http.route("/upabhokta-samiti/register", type="http", website=True, auth="user")
    def upabhokta_samiti_register_form(self):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        upabhokta_samiti_info = (
            http.request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )

        upabhokta_samiti_other_details = {
            "contact_person_name_": http.request.env.user.partner_id.name,
            "contact_person_phone_": http.request.env.user.phone,
            "contact_person_email_": http.request.env.user.email,
            "upabhokta_samiti_category_name": http.request.env.user.upabhokta_samiti_category.category,
            "upabhokta_samiti_category_id": http.request.env.user.upabhokta_samiti_category.id,
        }

        representatives_designations = (
            http.request.env["organization.designation.representative"]
            .sudo()
            .search([])
        )
        org_designations = (
            http.request.env["organization.designation.organization"].sudo().search([])
        )
        yojana_type = http.request.env["org.yojana.type"].sudo().search([])
        budget_type = http.request.env["org.budget.type"].sudo().search([])

        bank_bank_accounts = (
            http.request.env["upabhokta.samiti.bank.account"].sudo().search([])
        )
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_register_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "upabhokta_samiti_info": upabhokta_samiti_info,
                "representatives_designations": representatives_designations,
                "org_designations": org_designations,
                "yojana_type": yojana_type,
                "budget_type": budget_type,
                "bank_bank_accounts": bank_bank_accounts,
                "upabhokta_samiti_other_details": upabhokta_samiti_other_details,
            },
        )

    # Members Detail Page
    #  GET: /upabhokta-samiti/member-details
    @http.route(
        "/upabhokta-samiti/member-details", type="http", website=True, auth="user"
    )
    def upabhokta_samiti_members_detail_form(self):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        upabhokta_samiti_info = (
            http.request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        upabhokta_samiti_members_detail = (
            request.env["upabhokta.samiti.formation.members"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )

        org_designations = (
            http.request.env["organization.designation.organization"].sudo().search([])
        )

        return request.render(
            "upabhokta_samiti.upabhokta_samiti_members_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "upabhokta_samiti_info": upabhokta_samiti_info,
                "org_designations": org_designations,
                "upabhokta_samiti_members_detail": upabhokta_samiti_members_detail,
            },
        )

    # Individual Member Details Page
    #  GET: /upabhokta-samiti/member-details/{id}
    @http.route(
        "/upabhokta-samiti/member-details/<int:id>",
        methods=["GET"],
        type="http",
        website=True,
        auth="user",
    )
    def upabhokta_samiti_members_detail(self, id, **data):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        upabhokta_samiti_info = (
            http.request.env["upabhokta.samiti.info"].sudo().search([])
        )
        upabhokta_samiti_members_detail = (
            request.env["upabhokta.samiti.formation.members"]
            .sudo()
            .search([("id", "=", id)], limit=1)
        )

        org_designations = (
            http.request.env["organization.designation.organization"].sudo().search([])
        )

        return request.render(
            "upabhokta_samiti.upabhokta_samiti_members_view_details_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "upabhokta_samiti_info": upabhokta_samiti_info,
                "org_designations": org_designations,
                "upabhokta_samiti_members_detail": upabhokta_samiti_members_detail,
            },
        )

    # PUT: /upabhokta-samiti/member-details/update
    @http.route(
        "/upabhokta-samiti/member-details/update",
        methods=["POST"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def upabhokta_samiti_members_detail_update(self, **form_data):
        member_id = form_data.get("upabhokta_samiti_member_id")
        member_details = http.request.env["upabhokta.samiti.formation.members"].search(
            [("id", "=", member_id)], limit=1
        )

        # Get the attachment from the form request
        # Check if the attachment is null
        # If null then save the old data
        # And if there is data coming then encode the data and save the new data
        member_signature = form_data.get("signature")
        member_signature_attachment = member_signature.read()
        if member_signature is None or member_signature.filename == "":
            member_signature_attachment = member_details.member_signature
        else:
            member_signature_attachment = base64.b64encode(member_signature_attachment)

        member_picture = form_data.get("profile")
        member_picture_attachment = member_picture.read()
        if member_picture is None or member_picture.filename == "":
            member_picture_attachment = member_details.member_picture
        else:
            member_picture_attachment = base64.b64encode(member_picture_attachment)

        if member_details:
            new_member_details = {
                "member_full_name": form_data.get("upabhokta_samiti_member_name"),
                "samiti_member_designation": form_data.get("palika_org_designation"),
                "member_gender": form_data.get("upabhokta_samiti_member_gender"),
                "member_address": form_data.get("member_address"),
                "member_father_name": form_data.get("father_name"),
                "member_grandfather_name": form_data.get("grandfather_name"),
                "member_mobile": form_data.get("mobile"),
                "member_telephone_opt": form_data.get("telephone"),
                "member_citizenship_number": form_data.get("citizenship_number"),
                "member_citizenship_issued_district": form_data.get("issued_district"),
                "member_citizenship_issued_date_bs": form_data.get("issued_date_bs"),
                "member_signature": member_signature_attachment,
                "member_picture": member_picture_attachment,
            }

            response = member_details.sudo().write(new_member_details)
            print(form_data.get("palika_org_designation"))
        return request.redirect("/upabhokta-samiti/member-details")

    # GET: /upabhokta-samiti/member-details/update
    @http.route(
        "/upabhokta-samiti/member-details/update/<int:id>",
        methods=["GET"],
        type="http",
        website=True,
        auth="user",
    )
    def upabhokta_samiti_members_detail_update_form(self, id, **data):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        upabhokta_samiti_info = (
            http.request.env["upabhokta.samiti.info"].sudo().search([])
        )
        upabhokta_samiti_members_detail = (
            request.env["upabhokta.samiti.formation.members"]
            .sudo()
            .search([("id", "=", id)], limit=1)
        )

        org_designations = (
            http.request.env["organization.designation.organization"].sudo().search([])
        )

        return request.render(
            "upabhokta_samiti.upabhokta_samiti_members_update_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "upabhokta_samiti_info": upabhokta_samiti_info,
                "org_designations": org_designations,
                "upabhokta_samiti_members_detail": upabhokta_samiti_members_detail,
            },
        )

    # POST: /upabhokta-samiti/register/upabhokta-samiti-details
    @http.route(
        "/upabhokta-samiti/register/upabhokta-samiti-details",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
        cors="*",
    )
    def upabhokta_samiti_details(self, **data):
        upabhokta_samiti_name = data.get("upabhokta_samiti_name")

        province = data.get("sabha_pradesh")
        district = data.get("sabha_district")
        municipality = data.get("sabha_palika")
        ward = data.get("sabha_ward")
        tole = data.get("sabha_tole")
        yojana_name = data.get("yojana_name")
        yojana_type = data.get("yojana_type")
        yojana_budget_npr = data.get("yojana_budget")
        yojana_budget_type = data.get("yojana_budget_type")
        bank_details = data.get("yojana_bank")
        upabhokta_samiti_logo = data.get("samiti_logo")
        attachment = upabhokta_samiti_logo.read()

        contact_person_name_ = data.get("contact_person_name_")
        contact_person_phone_ = data.get("contact_person_phone_")
        contact_person_email_ = data.get("contact_person_email_")

        current_user_id = request.env.user.id
        try:
            new_upabhokta_samiti = (
                http.request.env["upabhokta.samiti.info"]
                .sudo()
                .create(
                    {
                        "upabhokta_samiti_name": upabhokta_samiti_name,
                        "province": province,
                        "district": district,
                        "municipality": municipality,
                        "ward": ward,
                        "tole": tole,
                        "yojana_name": yojana_name,
                        "yojana_type": yojana_type,
                        "yojana_budget_npr": yojana_budget_npr,
                        "yojana_budget_type": yojana_budget_type,
                        "bank_details": bank_details,
                        "contact_person_name_": contact_person_name_,
                        "contact_person_phone_": contact_person_phone_,
                        "contact_person_email_": contact_person_email_,
                        "upabhokta_samiti_logo": base64.b64encode((attachment)),
                        "user_id": current_user_id,
                    }
                )
            )

            return http.Response(
                json.dumps(
                    {
                        "id": new_upabhokta_samiti.id,
                    }
                ),
                content_type="application/json",
            )

        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                status=400,  # Bad Request status code
                content_type="application/json",
            )

    # PUT: /upabhokta-samiti/upabhokta-samiti-details/update
    @http.route(
        "/upabhokta-samiti/upabhokta-samiti-details/update",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
        cors="*",
    )
    def update_upabhokta_samiti(self, **data):
        samiti_update_id = data.get("samiti_update_id")
        # Record to update
        record_to_update = request.env["upabhokta.samiti.info"].browse(samiti_update_id)

        upabhokta_samiti_name = data.get("upabhokta_samiti_name")
        sabha_number = data.get("upabhokta_samiti_nth")
        registration_date_bs = data.get("sabha_date_bs")
        sabha_time = data.get("sabha_time")
        sabha_chairman_fullname = data.get("upabhokta_samiti_guest_chairman")
        palika_representative_designation = data.get(
            "palika_representative_designation"
        )
        palika_representative_name = data.get("palika_representative_name")
        province = data.get("sabha_pradesh")
        district = data.get("sabha_district")
        municipality = data.get("sabha_palika")
        ward = data.get("sabha_ward")
        tole = data.get("sabha_tole")
        yojana_name = data.get("yojana_name")
        yojana_type = data.get("yojana_type")
        yojana_budget_npr = data.get("yojana_budget")
        yojana_budget_type = data.get("yojana_budget_type")
        bank_details = data.get("yojana_bank")
        chief_guest = data.get("bisesh_athiti_full_name")
        total_attendees = data.get("sabha_attendees_number")
        upabhokta_samiti_logo = data.get("samiti_logo")
        project_proposal = data.get("project_proposal")
        if record_to_update:
            new_record = {
                "upabhokta_samiti_name": upabhokta_samiti_name,
                "sabha_number": sabha_number,
                "registration_date_bs": registration_date_bs,
                "sabha_time": sabha_time,
                "sabha_chairman_fullname": sabha_chairman_fullname,
                "palika_representative_designation": palika_representative_designation,
                "palika_representative_name": palika_representative_name,
                "province": province,
                "district": district,
                "municipality": municipality,
                "ward": ward,
                "tole": tole,
                "yojana_name": yojana_name,
                "yojana_type": yojana_type,
                "yojana_budget_npr": yojana_budget_npr,
                "yojana_budget_type": yojana_budget_type,
                "bank_details": bank_details,
                "chief_guest": chief_guest,
                "total_attendees": total_attendees,
                "upabhokta_samiti_logo": upabhokta_samiti_logo,
                "project_proposal": project_proposal,
            }

            record_to_update.sudo().write(new_record)
            return request.redirect("/upabhokta-samiti/dashboard")

    # POST: /upabhokta-samiti/member-details/register
    @http.route(
        "/upabhokta-samiti/member-details/register",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
        cors="*",
    )
    def register_samiti_member(self, **form_data):
        member_full_name = form_data.get("upabhokta_samiti_member_name")
        member_designation = form_data.get("palika_org_designation")
        member_gender = form_data.get("upabhokta_samiti_member_gender")
        member_address = form_data.get("member_address")
        member_father_name = form_data.get("father_name")
        member_grandfather_name = form_data.get("grandfather_name")
        member_mobile = form_data.get("mobile")
        member_telephone_opt = form_data.get("telephone")
        member_citizenship_number = form_data.get("citizenship_number")
        member_citizenship_issued_district = form_data.get("issued_district")
        member_citizenship_issued_date_bs = form_data.get("issued_date_bs")

        member_signature = form_data.get("signature")
        member_signature_attachment = member_signature.read()

        member_picture = form_data.get("profile")
        member_picture_attachment = member_picture.read()
        current_user_id = request.env.user.id
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        try:
            new_upabhokta_samiti_member = (
                http.request.env["upabhokta.samiti.formation.members"]
                .sudo()
                .create(
                    {
                        "member_full_name": member_full_name,
                        "samiti_member_designation": member_designation,
                        "member_gender": member_gender,
                        "member_address": member_address,
                        "member_father_name": member_father_name,
                        "member_grandfather_name": member_grandfather_name,
                        "member_mobile": member_mobile,
                        "member_telephone_opt": member_telephone_opt,
                        "member_citizenship_number": member_citizenship_number,
                        "member_citizenship_issued_district": member_citizenship_issued_district,
                        "member_citizenship_issued_date_bs": member_citizenship_issued_date_bs,
                        "member_signature": base64.b64encode(
                            member_signature_attachment
                        ),
                        "member_picture": base64.b64encode(member_picture_attachment),
                        "samiti_formation_members_reference_page_id": page,
                        "user_id": current_user_id,
                    }
                )
            )
            return request.redirect("/upabhokta-samiti/member-details")
        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                status=400,  # Bad Request status code
                content_type="application/json",
            )

    # GET: Sabha Details Page
    @http.route(
        "/upabhokta-samiti/sabha-details",
        methods=["GET"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_sabha_details_page(self, **data):
        sabha_details = (
            request.env["upabhokta.samiti.sabha.details"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        representatives_designations = (
            http.request.env["organization.designation.representative"]
            .sudo()
            .search([])
        )
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_sabha_details_template",
            {
                "representatives_designations": representatives_designations,
                "sabha_details": sabha_details,
            },
        )

    # POST: /upabhokta-samiti/sabha-details/register
    @http.route(
        "/upabhokta-samiti/sabha-details/register",
        methods=["POST"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def register_sabha_details(self, **data):
        sabha_number = data.get("upabhokta_samiti_nth")
        sabha_date_bs = data.get("sabha_date_bs")
        sabha_time = data.get("sabha_time")
        sabha_chairman_fullname = data.get("upabhokta_samiti_guest_chairman")
        palika_representative_designation = data.get(
            "palika_representative_designation"
        )
        palika_representative_name = data.get("palika_representative_name")
        chief_guest = data.get("bisesh_athiti_full_name")
        total_attendees = data.get("sabha_attendees_number")
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id

        sabha_record = {
            "sabha_number": sabha_number,
            "sabha_date_bs": sabha_date_bs,
            "sabha_time": sabha_time,
            "sabha_chairman_fullname": sabha_chairman_fullname,
            "palika_representative_designation": palika_representative_designation,
            "palika_representative_name": palika_representative_name,
            "chief_guest": chief_guest,
            "total_attendees": total_attendees,
            "samiti_sabha_details_reference_page_id": page,
        }

        request.env["upabhokta.samiti.sabha.details"].sudo().create(sabha_record)

        return http.Response(
            json.dumps(sabha_record),
            status=404,
            content_type="application/json",
        )

    # Project Proposal Main Page
    @http.route(
        "/upabhokta-samiti/project-proposals/",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def page_project_proposals(self):
        document = (
            request.env["upabhokta.samiti.project.proposal"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_project_proposals_template",
            {"document": document},
        )

    # POST: /upabhokta-samiti/project-proposal
    @http.route(
        "/upabhokta-samiti/project-proposals/create",
        methods=["POST"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def post_project_proposal(self, **data):
        proposal_text = data.get("editor")
        signed_document = data.get("signed_document")
        signed_document_data = signed_document.read()
        document_name = signed_document.filename
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        response = (
            request.env["upabhokta.samiti.project.proposal"]
            .sudo()
            .create(
                {
                    "proposal_text": proposal_text,
                    "signed_document": base64.b64encode(signed_document_data),
                    "document_name": document_name,
                    "page_ref": page,
                }
            )
        )

        if response:
            return http.Response(
                json.dumps(
                    {
                        "recordID": response.id,
                        "status": 400,
                    }
                ),
                status=404,
                content_type="application/json",
            )

    # Project Proposal Main Page
    @http.route(
        "/upabhokta-samiti/bank-request/",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def page_bank_request(self):
        document = (
            request.env["upabhokta.samiti.project.bankreq"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_Bank_Request_template",
            {"document": document},
        )

    # Bank Account Request
    @http.route(
        "/upabhokta-samiti/bank-request/create",
        methods=["POST"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def post_bank_request(self, **data):
        request_text = data.get("editor")
        signed_document = data.get("signed_document")
        signed_document_data = signed_document.read()
        document_name = signed_document.filename
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        response = (
            request.env["upabhokta.samiti.project.bankreq"]
            .sudo()
            .create(
                {
                    "bank_request_doc_text": request_text,
                    "signed_document": base64.b64encode(signed_document_data),
                    "document_name": document_name,
                    "page_ref": page,
                }
            )
        )

        if response:
            return http.Response(
                json.dumps(
                    {
                        "recordID": response.id,
                        "status": 400,
                    }
                ),
                status=404,
                content_type="application/json",
            )

    # Delete Member
    @http.route(
        "/upabhokta-samiti/member-details/delete/<int:id>",
        methods=["DELETE"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def delete_samiti_member(self, id):
        # Get record with matching id
        member_model = (
            request.env["upabhokta.samiti.formation.members"].sudo().browse(id)
        )
        # If there is record with id
        if member_model:
            member_model.unlink()
            return request.redirect("/upabhokta-samiti/member-details")

    # Attendees
    # Get Attendees Page
    @http.route(
        "/upabhokta-samiti/attendee-details",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_attendees_details(self):
        attendees_list = (
            request.env["upabhokta.samiti.attendees"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_attendees_template",
            {"attendees_list": attendees_list},
        )

    # Post Attendees Form Data
    @http.route(
        "/upabhokta-samiti/attendees/register",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def post_attendees_details(self, **form_data):
        upabhokta_samiti_attendees_name = form_data.get(
            "upabhokta_samiti_attendees_name"
        )
        upabhokta_samiti_attendees_gender = form_data.get(
            "upabhokta_samiti_attendees_gender"
        )
        signature = form_data.get("signature")
        signature_file = signature.read()
        mobile = form_data.get("mobile")
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        request.env["upabhokta.samiti.attendees"].sudo().create(
            {
                "full_name": upabhokta_samiti_attendees_name,
                "signature": base64.b64encode(signature_file),
                "mobile": mobile,
                "gender": upabhokta_samiti_attendees_gender,
                "attendees_id": page,
            }
        )
        return request.redirect("/upabhokta-samiti/attendee-details")

    # Return Beneficiary Page
    @http.route(
        "/upabhokta-samiti/beneficiary",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_beneficiary_details(self):
        beneficiary_list = (
            request.env["upabhokta.samiti.beneficiary.record"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        category = request.env["upabhokta.samiti.beneficiary.master"].sudo().search([])
        return request.render(
            "upabhokta_samiti.upabhokta_samiti_beneficiary_template",
            {"category": category, "beneficiary_list": beneficiary_list},
        )

    # Beneficiary Form Request
    @http.route(
        "/upabhokta-samiti/beneficiary/create",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def create_beneficiary_details(self, **form_data):
        category_name = form_data.get("category_name")
        category_male_population = form_data.get("category_male_population")
        category_female_population = form_data.get("category_female_population")
        category_family_numbers = form_data.get("category_family_numbers")
        page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page_ref = page.id
        new_beneficiary = {
            "category": category_name,
            "category_male_population": category_male_population,
            "category_female_population": category_female_population,
            "category_family_numbers": category_family_numbers,
            "page_ref": page_ref,
        }
        print(new_beneficiary)
        request.env["upabhokta.samiti.beneficiary.record"].sudo().create(
            new_beneficiary
        )
        return request.redirect("/upabhokta-samiti/beneficiary")

    # Beneficiary Update
    @http.route(
        "/upabhokta-samiti/beneficiary/update",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def update_beneficiary_details(self, **form_data):
        beneficiary_id = form_data.get("beneficiary_id")
        old_data = (
            request.env["upabhokta.samiti.beneficiary"].sudo().browse(beneficiary_id)
        )

        new_beneficiary = {
            "tribal_male_population": form_data.get("tribal_male_population"),
            "tribal_female_population": form_data.get("tribal_female_population"),
            "tribal_family_number": form_data.get("tribal_family_number"),
            "dalit_male_population": form_data.get("dalit_male_population"),
            "dalit_female_population": form_data.get("dalit_female_population"),
            "dalit_family_number": form_data.get("dalit_family_number"),
            "children_male_population": form_data.get("children_male_population"),
            "children_female_population": form_data.get("children_female_population"),
            "total_child_population": form_data.get("total_child_population"),
            "other_community_male_population": form_data.get(
                "other_community_male_population"
            ),
            "other_community_female_population": form_data.get(
                "other_community_female_population"
            ),
            "other_community_family_number": form_data.get(
                "other_community_family_number"
            ),
            "total_family_numbers": form_data.get("total_family_numbers"),
            "total_population": form_data.get("total_population"),
            "total_male_population": form_data.get("total_male_population"),
            "total_female_population": form_data.get("total_female_population"),
        }

        if old_data:
            old_data.sudo().write(new_beneficiary)
        return request.redirect("/upabhokta-samiti/beneficiary")

    # Return Anugaman Team Page
    @http.route(
        "/upabhokta-samiti/anugaman-team-member",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_anugaman_team_details(self):
        # Fetch anugaman members
        anugaman_team_members = (
            request.env["upabhokta.samiti.anugaman.team"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        samiti_members_details = (
            request.env["upabhokta.samiti.formation.members"]
            .sudo()
            .search(
                [
                    ("create_uid", "=", http.request.env.user.id),
                ]
            )
        )

        return request.render(
            "upabhokta_samiti.upabhokta_samiti_anugaman_members_template",
            {
                "samiti_members_details": samiti_members_details,
                "anugaman_team_members": anugaman_team_members,
            },
        )

    # POST: upabhokta-samiti/anugaman-team-member/register
    @http.route(
        "/upabhokta-samiti/anugaman-team-member/register",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def post_anugaman_team_member_details(self, **form_data):
        member_id = form_data.get("anugaman_team_member")

        # get the member info from formation member table
        formation_member = (
            request.env["upabhokta.samiti.formation.members"]
            .sudo()
            .search([("id", "=", member_id)], limit=1)
        )
        _page = (
            request.env["upabhokta.samiti.info"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id

        if formation_member:
            new_anugaman_team_member = {
                "full_name": formation_member.id,
                "anugaman_member_designation": formation_member.samiti_member_designation.id,
                "member_gender": formation_member.member_gender,
                "member_address": formation_member.member_address,
                "member_mobile": formation_member.member_mobile,
                "member_telephone_opt": formation_member.member_telephone_opt,
                "member_citizenship_number": formation_member.member_citizenship_number,
                "member_citizenship_issued_district": formation_member.member_citizenship_issued_district.id,
                "member_citizenship_issued_date_bs": formation_member.member_citizenship_issued_date_bs,
                "notebook_reference_id": page,
            }

            request.env["upabhokta.samiti.anugaman.team"].sudo().create(
                new_anugaman_team_member
            )

        return request.redirect("/upabhokta-samiti/anugaman-team-member")

    # Delete Anugaman Team Member
    # DELETE: /upabhokta-samiti/anugaman-team-member/{id}
    @http.route(
        "/upabhokta-samiti/anugaman-team-member/delete/<int:id>",
        methods=["DELETE"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def delete_anugaman_team_member(self, id):
        # Get record with matching id
        member_model = request.env["upabhokta.samiti.anugaman.team"].sudo().browse(id)
        # If there is record with id
        if member_model:
            member_model.unlink()
            return request.redirect("/upabhokta-samiti/anugaman-team-member")


class UserNotification(http.Controller):
    @http.route(
        "/upabhokta-samiti/user/notification/<int:id>",
        methods=["GET"],
        type="http",
        auth="user",
        website=True,
    )
    def user_notification(self, id):
        unread_notification = (
            request.env["upabhokta.samiti.notification"]
            .sudo()
            .search(
                [
                    ("id", "=", id),
                    ("sent_to", "=", http.request.env.user.id),
                    ("status", "=", False), 
                ]
            )
        )

        read_notification = unread_notification.sudo().write({"status": True})

        return request.redirect("/upabhokta-samiti/dashboard")
    
    
    @http.route("/test",type="http",website=True,auth="public")
    def test_func(self):
        return request.render("upabhokta_samiti.test_view",{})
