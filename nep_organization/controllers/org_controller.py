from odoo import http
from odoo.http import request
import base64
import json



class OrganizationController(http.Controller):
    # Dashboard
    @http.route(
        ["/organization", "/organization/dashboard"],
        type="http",
        website=True,
        auth="user",
    )
    def get_dashboard(self):
        return request.render("nep_organization.org_dashboard_template_", {})

    # GET|POST: /organization/basic-details
    @http.route(
        ["/organization/basic-details"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def org_basic_details(self, province_id=None, **data):
        if not province_id:
            return []
        organization_categories = request.env["organization.type"].sudo().search([])
        districts = request.env["location.district"].sudo().search(['province_name', '=', province_id])
        provinces = request.env["location.province"].sudo().search([])
        palika = request.env["location.palika"].sudo().search([])
        org_designations = (
            request.env["organization.designation.organization"].sudo().search([])
        )
        check_if_organization_exists = (
            request.env["organization.information"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        fiscal_year = request.env["fiscal.year"].sudo().search([])
        org_external_details = {
            "organization_categories": organization_categories,
            "districts": districts,
            "provinces": provinces,
            "palika": palika,
            "contact_person_name_": http.request.env.user.partner_id.name,
            "contact_person_phone_": http.request.env.user.phone,
            "contact_person_email_": http.request.env.user.email,
            "contact_person_designation": org_designations,
            # "org_category_name": http.request.env.user.organization_category.category,
            "fiscal_year": fiscal_year,
            # "org_category_id": http.request.env.user.organization_category.id,
        }

        if request.httprequest.method == "POST":
            organization_logo_raw = data.get("org_logo").read()
            organization_logo_binary = base64.b64encode(organization_logo_raw)

            inserted_data = {
                "org_name_en": data.get("organization_name_en"),
                "org_name_np": data.get("organization_name_np"),
                "org_shortcut_name": data.get("organization_short_form_name"),
                "org_category": data.get("organization_category"),
                "organization_type": data.get("organization_type"),
                "contact_person_name_": data.get("contact_person_name_"),
                "contact_person_phone_": data.get("contact_person_phone_"),
                "contact_person_email_": data.get("contact_person_email_"),
                "contact_person_designation": data.get("contact_person_designation"),
                "org_province": data.get("gathan_pradesh"),
                "org_district": data.get("gathan_district"),
                "org_municipality": data.get("gathan_palika"),
                "org_ward": data.get("gathan_ward"),
                "org_tole": data.get("gathan_tole"),
                "org_email": data.get("org_email"),
                "org_telephone": data.get("org_telephone"),
                "org_postbox_number": data.get("org_post_box"),
                "org_fax_number": data.get("org_fax"),
                "org_house_number": data.get("org_house_number"),
                "org_website_url": data.get("org_website"),
                "organization_logo": organization_logo_binary,
            }

            request.env["organization.information"].sudo().create(inserted_data)
            return request.redirect("/organization/basic-details")

        return request.render(
            "nep_organization.org_basic_details_template",
            {
                "org_external_details": org_external_details,
                "check_if_organization_exists": check_if_organization_exists,
            },
        )

    # GET|POST: /organization/meeting-details
    @http.route(
        ["/organization/meeting-details"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def org_meeting_details(self, **data):
        sabha_details = (
            request.env["organization.sabha.details"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )

        if request.httprequest.method == "POST":
            sabha_number = data.get("organization_nth")
            sabha_date_bs = data.get("sabha_date_bs")
            sabha_time = data.get("sabha_time")
            sabha_chairman_fullname = data.get("organization_guest_chairman")
            chief_guest = data.get("bisesh_athiti_full_name")
            total_attendees = data.get("sabha_attendees_number")
            _page = (
                request.env["organization.information"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
            page = _page.id

            sabha_record = {
                "sabha_number": sabha_number,
                "sabha_date_bs": sabha_date_bs,
                "sabha_time": sabha_time,
                "sabha_chairman_fullname": sabha_chairman_fullname,
                "chief_guest": chief_guest,
                "total_attendees": total_attendees,
                "sanstha_details_reference_page_id": page,
            }

            request.env["organization.sabha.details"].sudo().create(sabha_record)
            return print("Data received.")

        return request.render(
            "nep_organization.org_meeting_details_template",
            {
                "sabha_details": sabha_details,
            },
        )
   
    @http.route(
        "/organization/purposes",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def page_project_proposals(self):
        document = (
            request.env["organization.purpose"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        return request.render("nep_organization.org_purpose_template", {'document': document})


    # 

    # GET|POST: /organization/purposes
    @http.route(
        ["/organization/purposes/create"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def org_purposes(self, **data):
        if request.httprequest.method == "POST":
            purpose_text = data.get("editor")
            signed_document = data.get("signed_document")
            signed_document_data = signed_document.read()
            document_name = signed_document.filename
            _page = (
                request.env["organization.information"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )
        

            page = _page.id
            response = (
                request.env["organization.purpose"]
                .sudo()
                .create(
                    {
                        "purpose_text": purpose_text,
                        "signed_document": base64.b64encode(signed_document_data),
                        "document_name": document_name,
                        "page_ref": page,
                    }
                )
            )
            if response:
                return request.redirect("/organization/purposes")


    # GET|POST: /organization/members
    @http.route(
        ["/organization/member-details"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def org_members(self, **data):
        nep_districts = http.request.env["location.district"].sudo().search([])
        nep_province = http.request.env["location.province"].sudo().search([])
        nep_palika = http.request.env["location.palika"].sudo().search([])
        qualifications = http.request.env["member.qualification.master"].sudo().search([])
        org_info = (
            http.request.env["organization.information"].sudo().search([])
        )
        members_detail = (
            request.env["organization.formation.members"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        org_designations = (
            http.request.env["org.representative.designation"].sudo().search([])
        )
        fiscal_year = request.env["fiscal.year"].sudo().search([])
        quota = http.request.env["quota.master"].sudo().search([])

        return request.render(
            "nep_organization.org_members_template",
            {
                "nep_districts": nep_districts,
                "nep_province": nep_province,
                "nep_palika": nep_palika,
                "org_info": org_info,
                "org_designations": org_designations,
                "fiscal_year": fiscal_year,
                "quota": quota,
                "members_detail": members_detail,
                "qualifications":qualifications,
            },
        )
    
    # Member create
    @http.route(
    "/organization/member-details/create",
    type="http",
    methods=["POST"],
    website=True,
    auth="user",
    csrf=False,
)
    def post_member_details(self, **form_data):
        member_full_name = form_data.get("member_full_name")
        member_gender = form_data.get("member_gender")
        organization_member_designation = form_data.get("organization_member_designation")      
        qualification = form_data.get("qualification")
        member_address = form_data.get("member_address")
        profile = form_data.get("profile")
        profile_file = profile.read()
        signature = form_data.get("signature")
        signature_file = signature.read()
        mobile = form_data.get("mobile")
        citizenship_number = form_data.get("citizenship_number")
        issued_district = form_data.get("issued_district")
        issued_date_bs = form_data.get("issued_date_bs")
        citizenship_front = form_data.get("citizenship_front")
        citizenship_front_img =citizenship_front.read()
        citizenship_back = form_data.get("citizenship_back")
        cirizenship_back_img = citizenship_back.read()
        telephone = form_data.get("telephone")
        email = form_data.get("email")
        father_name = form_data.get("father_name")
        mother_name = form_data.get("mother_name")
        grandfather_name = form_data.get("grandfather_name")
        member_tenure = form_data.get("member_tenure")
        member_type = form_data.get("member_type")
        status = form_data.get("status")

        current_user_id = request.env.user.id

        _page = (
            request.env["organization.information"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        request.env["organization.formation.members"].sudo().create(
            {
                'member_full_name': member_full_name,
                'member_gender': member_gender,
                'organization_member_designation': organization_member_designation,
                'qualification_level_': qualification,
                'member_address': member_address,
                'member_father_name': father_name,
                'member_mother_name': mother_name,
                'member_grandfather_name': grandfather_name,
                'member_mobile': mobile,
                'member_telephone_opt': telephone,
                "member_email":email,
                'member_citizenship_number': citizenship_number,
                'member_citizenship_issued_district': issued_district,
                'member_citizenship_issued_date_bs': issued_date_bs,
                'citizenship_front_image': base64.b64encode(citizenship_front_img),
                'citizenship_back_image': base64.b64encode(cirizenship_back_img),
                'member_signature': base64.b64encode(signature_file),
                'member_picture': base64.b64encode(profile_file),
                'comitte_member_tenure': member_tenure,
                'member_type': member_type,
                'status': status,
                'organization_formation_members_reference_page_id': page,
                'user_id': current_user_id,
            }
        )
        return request.redirect("/organization/member-details")

    
     # View: Fix Assets
    @http.route(
        "/organization/member-details/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def view_members(self, id):
        # Get record with matching id
        members_detail = request.env["organization.formation.members"].sudo().browse(id)
        # If there is record with id
        return http.request.render(
                    "nep_organization.view_members_template",
                    { "members_detail": members_detail},
                   
                )
        
    @http.route(
        "/organization/member-details/delete/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def delete_members(self, id):
        # Get record with matching id
        member_model = request.env["organization.formation.members"].sudo().browse(id)
        # If there is record with id
        if member_model:
            member_model.unlink()
            return request.redirect("/organization/member-details")

    
    
    
    
    
    
    
    
        

 # Attendees
    # Get Attendees Page
    @http.route(
        "/organization/attendee-details",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_attendees_details(self):
        attendees_list = (
            request.env["organization.attendees"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        return request.render(
            "nep_organization.organization_attendees_template",
            {"attendees_list": attendees_list},
        )

    # Post Attendees Form Data
    @http.route(
        "/organization/attendees/register",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def post_attendees_details(self, **form_data):
        organization_attendees_name = form_data.get(
            "organization_attendees_name"
        )
        organization_attendees_gender = form_data.get(
            "organization_attendees_gender"
        )
        organization_attendees_sabha = (
            request.env["organization.sabha.details"].sudo().search([])
        )
       
        organization_attendees_sabha_number = form_data.get( "organization_attendees_sabha_number")
        signature = form_data.get("signature")
        signature_file = signature.read()
        mobile = form_data.get("mobile")
        _page = (
            request.env["organization.information"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page = _page.id
        request.env["organization.attendees"].sudo().create(
            {
                "full_name": organization_attendees_name,
                "signature": base64.b64encode(signature_file),
                "mobile": mobile,
                "gender": organization_attendees_gender,
                "attendees_id": page,
                "sabha_name":organization_attendees_sabha_number
            }
        )
        return request.redirect("/organization/attendee-details")
    
    
      # Return Quota Page
    @http.route(
        "/organization/member/quota",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def get_quota_details(self):
        quota_list = (
            request.env["organization.member.quota"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        print(quota_list)
        category = request.env["quota.master"].sudo().search([])
        return request.render(
            "nep_organization.organization_quota_template",
            {"category": category, "quota_list": quota_list},
        )

    # Quota Form Request
    @http.route(
        "/organization/member/quota/create",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def create_quota_details(self, **form_data):
        category_name = form_data.get("category_name")
        category_total_numbers = form_data.get("category_total_numbers")
        page = (
            request.env["organization.information"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page_ref = page.id
        new_quota = {
            "category": category_name,
            "category_total_numbers": category_total_numbers,
            # "member_male_population": total_male_population,
            # "member_female_population": total_female_population,
            # "member_other_population": total_other_population,
            "page_ref": page_ref,
        }
       
        request.env["organization.member.quota"].sudo().create(
            new_quota
        )
        return request.redirect("/organization/member/quota")

    @http.route(
        "/organization/fix-assets",
        type="http",
        website=True,
        auth="user",
        csrf=False,
        
    )
    def get_fix_assets_details(self):
         
        asset_list = (
            request.env["organization.fix.assets"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        org_asset_type = request.env["org.asset.master"].sudo().search([]).read()

        org_external_details = {
                'org_asset_type': org_asset_type
            }
        return request.render(
                    "nep_organization.organization_asset_template",
                    {"org_asset_type": org_asset_type, "asset_list": asset_list},
                   
                )

     # Asset Form Request
    @http.route(
        "/organization/fix-assets/create",
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def create_fix_asset_details(self, **form_data):
        try:
            # org_asset_type = (
            #     request.env['org.asset.master']
            #     .sudo()
            #     .search([])
            # )
            

            page = (
                request.env["organization.information"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )

           
           
            asset_ref_id = page.id

            # Create a new_assets dictionary with common fields
            new_assets = {
                'asset_name': form_data.get("asset_name"),
                'location_of_asset': form_data.get("location_of_asset"),
                'asset_number': form_data.get("asset_number"),
                'asset_total_cost': form_data.get("asset_total_cost"),
                # Page reference
                'asset_ref_id': asset_ref_id
            }

            if form_data.get("asset_name") == '3':
                new_assets['total_kitta_number'] = form_data.get("total_kitta_number")
            elif form_data.get("asset_name") == '1':
                new_assets['no_of_rooms'] = form_data.get("no_of_rooms")
                new_assets['house_block_number'] = form_data.get("house_block_number")
            elif form_data.get("asset_name") == '2':
                new_assets['vehicle_type'] = form_data.get("vehicle_type")

            print(new_assets)
            print("Created................................")

            request.env["organization.fix.assets"].sudo().create(new_assets)

            return request.redirect("/organization/fix-assets")

        except Exception as e:
            # Handle the exception (e.g., log the error, show an error message)
            print(f"An error occurred: {str(e)}")
            # Optionally, you can raise the exception again if you want to propagate it further.
            raise


# DELETE: Fix Assets Delete
    @http.route(
        "/organization/fix-assets/delete/<int:id>",
        methods=["DELETE"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def delete_fix_assets(self, id):
        # Get record with matching id
        assets_model = request.env["organization.fix.assets"].sudo().browse(id)
        # If there is record with id
        if assets_model:
            assets_model.unlink()
            return request.redirect("/organization/fix-assets")

 


    @http.route(
        "/organization/program-details",
        type="http",
        website=True,
        auth="user",
        csrf=False,
        
    )
    def get_program_details(self):
         
        program_list = (
            request.env["organization.program.record"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)])
        )
        
        return request.render(
                    "nep_organization.org_program_details_template",
                    { "program_list": program_list},
                   
                )

 # POST: /organization/program-details
    @http.route(
        ["/organization/program-details/create"],
        type="http",
        methods=["POST"],
        website=True,
        auth="user",
        csrf=False,
    )
    def org_program_details(self, **data):
        program_collaborative_organization = request.env["collaborative.org.master"].sudo().search([])
        page = (
            request.env["organization.information"]
            .sudo()
            .search([("create_uid", "=", http.request.env.user.id)], limit=1)
        )
        page_ref = page.id
        
       
        

        inserted_data = {
            "program_name": data.get("program_name"),
            "program_purpose": data.get("program_purpose"),
            "program_chairman_fullname": data.get("program_chairman_fullname"),
            "program_location": data.get("program_location"),
            "program_start_time": data.get("program_start_time"),
            "program_end_time": data.get("program_end_time"),
            "program_budget": data.get("program_budget"),
            "program_collaborative_organization": data.get("program_collaborative_organization"),
            "page_ref": page_ref,
                    
        }
        

        request.env["organization.program.record"].sudo().create(inserted_data)
        return request.redirect("/organization/program-details")

# Delete Program Details
    @http.route(
        "/organization/program-details/delete/<int:id>",
        methods=["DELETE"],
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def delete_program(self, id):
        # Get record with matching id
        program_model = request.env["organization.program.record"].sudo().browse(id)
        # If there is record with id
        if program_model:
            program_model.unlink()
            return request.redirect("/organization/program-details")

 


    # View: Fix Assets
    @http.route(
        "/organization/fix-assets/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def view_fix_assets(self, id):
        # Get record with matching id
        asset = request.env["organization.fix.assets"].sudo().browse(id)
        # If there is record with id
        return http.request.render(
                    "nep_organization.view_fix_assets_template",
                    { "asset": asset},
                   
                )
        
    # Edit: Fix Assets
    @http.route(
        "/organization/edit-fix-assets/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def update_fix_assets(self, id):
        asset = request.env["organization.fix.assets"].sudo().browse(id)
        org_asset_type = request.env["org.asset.master"].sudo().search([])
        for asset_name in org_asset_type:
            if asset_name.org_asset_type == asset.asset_name.org_asset_type:
                value = asset_name
                print(value)
            
       
        
        return http.request.render(
                    "nep_organization.edit_fix_assets_template",
                    { "asset": asset,
                     'org_asset_type': org_asset_type,},
                   
                )
        
# Update 
    @http.route(
            "/organization/fix-assets/update",
            type="http",
            methods=["POST"],
            website=True,
            auth="user",
            csrf=False,
        )
    
    def edit_fix_assets(self, **form_data):
        try:
            # org_asset_type = (
            #     request.env['org.asset.master']
            #     .sudo()
            #     .search([])
            # )
            

            page = (
                request.env["organization.information"]
                .sudo()
                .search([("create_uid", "=", http.request.env.user.id)], limit=1)
            )

           
           
            asset_ref_id = page.id

            # Create a new_assets dictionary with common fields
            asset_id=form_data.get('asset_id') 
            asset_sd = form_data.get('asset_name'),
            location_of_asset=form_data.get("location_of_asset")
            asset_number=form_data.get("asset_number")
            asset_total_cost=form_data.get("asset_total_cost"),
            total_kitta_number = form_data.get("total_kitta_number"),
            no_of_rooms = form_data.get("no_of_rooms"),
            house_block_number = form_data.get("house_block_number"),
            vehicle_type = form_data.get("vehicle_type"),
            print("..............................")
            print(f"Asset details: {asset_sd},{location_of_asset}, {asset_number}, {type(asset_sd)}")
            # asset_name_int = int(asset_name) 
            # print(f"Asset type int: {asset_name_int}, {asset_name_int}")
            Asset = request.env["organization.fix.assets"].sudo()
            
            asset = Asset.browse(int(asset_id))
           
           
            asset.write({
                'asset_name':asset_sd,
                'location_of_asset':location_of_asset,
                'asset_number':asset_number,
                'asset_total_cost':asset_total_cost,
                'total_kitta_number': total_kitta_number,
                'no_of_rooms':no_of_rooms,
                'house_block_number': house_block_number,
                'vehicle_type': vehicle_type
                
                
                
            })
            
            

            return request.redirect("/organization/fix-assets")

        except Exception as e:
            # Handle the exception (e.g., log the error, show an error message)
            print(f"An error occurred: {str(e)}")
            # Optionally, you can raise the exception again if you want to propagate it further.
            raise

    # Program Details: View
    @http.route(
        "/organization/program-details/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def view_members(self, id):
        # Get record with matching id
        programs_detail = request.env["organization.program.record"].sudo().browse(id)
        # If there is record with id
        return http.request.render(
                    "nep_organization.org_program_details_view",
                    { "programs_detail": programs_detail},
        )
    

    # Program Details: Edit
    @http.route(
        "/organization/program-details/edit/<int:id>",
        type="http",
        website=True,
        auth="user",
        csrf=False,
    )
    def view_members(self, id):
        # Get record with matching id
        programs_detail = request.env["organization.program.record"].sudo().browse(id)
        # If there is record with id
        return http.request.render(
                    "nep_organization.org_program_details_edit",
                    { "programs_detail": programs_detail},
        )
        
    