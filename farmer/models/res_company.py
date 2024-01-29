from odoo import models,fields,_,api
import nepali_datetime 

class CompanyServiceType(models.Model):
    _name = 'company.service.type'
    _description = 'Compnay Serive Type'

    name = fields.Char(string=_("Name"))

class ResCompanyDetails(models.Model):
    _name = 'res.company.details'
    _description = 'Company Details'

    parent_id = fields.Many2one("res.company",string=_("Company"))
    url = fields.Char("Web URL",unique=True)
    khalti_api_key = fields.Char(_("Khalti API key"))
    esewa_merchant_code = fields.Char(_("Esewa Merchant Code"))
    service_type = fields.Many2one("company.service.type")
    start_date_ad = fields.Date(string=_('Start Date(A.D)'),required=False,compute = '_sync_start_date_ad_bs_date',store=True)
    start_date_bs = fields.Char(string=_('Start Date(B.S.)'),required=False,compute = '_sync_start_date_bs_ad_date',store=True)

    khalti_api_key = fields.Char(_("Khalti API key"))
    esewa_merchant_code = fields.Char(_("Esewa Merchant Code")) 

    khalti_api_key_exists = fields.Boolean(compute="compute_khalti_api_key_exists")
    esewa_merchant_code_exits = fields.Boolean(compute="compute_esewa_merchant_code_exits")

    def compute_khalti_api_key_exists(self):
        for record in self:
            if record.khalti_api_key:
                self.khalti_api_key_exists = True

    def compute_esewa_merchant_code_exits(self):
        for record in self:
            if record.esewa_merchant_code:
                self.esewa_merchant_code_exits = True



    @api.onchange('start_date_ad')
    def _sync_start_date_bs_ad_date(self):
        for record in self:
            if not record.start_date_ad:
                record.start_date_bs = nepali_datetime.date.today()
            else:
                record.start_date_bs = nepali_datetime.date.from_datetime_date(record.start_date_ad)

    @api.onchange('start_date_bs')
    def _sync_start_date_ad_bs_date(self):
        for record in self:
            if not record.start_date_bs:
                record.start_date_ad = nepali_datetime.date.today()
            else:
                nepali_date = nepali_datetime.datetime.strptime(record.start_date_bs, '%Y-%m-%d')
                english_date = nepali_date.to_datetime_date()
                record.start_date_ad = english_date

    expiry_date_ad = fields.Date(string=_('Expiry Date(A.D)'),required=False,compute = '_sync_expiry_date_ad_bs_date',store=True)
    expiry_date_bs = fields.Char(string=_('Expiry Date(B.S.)'),required=False,compute = '_sync_expiry_date_bs_ad_date',store=True)

    @api.onchange('expiry_date_ad')
    def _sync_expiry_date_bs_ad_date(self):
        for record in self:
            if not record.expiry_date_ad:
                record.expiry_date_bs = nepali_datetime.date.today()
            else:
                record.expiry_date_bs = nepali_datetime.date.from_datetime_date(record.expiry_date_ad)

    @api.onchange('expiry_date_bs')
    def _sync_expiry_date_ad_bs_date(self):
        for record in self:
            if not record.expiry_date_bs:
                record.expiry_date_ad = nepali_datetime.date.today()
            else:
                nepali_date = nepali_datetime.datetime.strptime(record.expiry_date_bs, '%Y-%m-%d')
                english_date = nepali_date.to_datetime_date()
                record.expiry_date_ad = english_date

class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Company'
    _sql_constraints =[('unique_code_per_comp','unique(id,code)','Company Code already Taken')]

    is_local_entity = fields.Boolean("Is local entity",default=True)
    is_producer_entity = fields.Boolean("Is Producer entity",default=False)
    # company_domain_name = fields.Char(string=_("Company Domain"))
    company_detail_ids = fields.One2many("res.company.details","parent_id",string=_("Company Details"))
    # Location Information
    province = fields.Many2one('location.province',string=_('Province'),required=True)
    district = fields.Many2one('location.district',string=_('District'),require=True)
    palika = fields.Many2one('location.palika',string=_('Palika'),required=True)
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))
    full_address = fields.Char("Address",compute="_compute_full_address")
    show_tax = fields.Boolean("Show tax in invoice",default=True)
    login_bg_img = fields.Binary("Login Background Image",required=True)

    def _compute_full_address(self):
        for record in self:
            temp=""
            if record.palika:
                temp+=record.palika.palika_name
            if record.ward_no:
                temp+=' - '+record.ward_no+', '
            if record.district:
                temp+=record.district.district_name+', '
            if record.province:
                temp+=record.province.name
            
            record.full_address = temp


    company_code = fields.Char(string=_('Company Code'),required=True,size=15)
    fax_number = fields.Char(string=_('Fax Number'),required=False)
    pan_number = fields.Char(string=_('PAN Number'),required=False)
    name_np = fields.Char(string=_('Company Nepali Name'),required=True)

    @api.onchange('province')
    def _clear_province_name(self):
        if self.district.province_name!=self.province:
            self.district=None
        if self.palika.district_name!=self.district:
            self.palika=None

    @api.onchange('district')
    def _clear_district_name(self):
        if self.district.district_name!=self.district:
            self.palika=None

    def _create_farmer_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Code' % company.name,
                'code': 'farmer.sequence',
                'company_id': company.id,
                'prefix': 'FR-80',
                'padding': 6,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_group_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Group Code' % company.name,
                'code': 'farmer.group.sequence',
                'company_id': company.id,
                'prefix': 'FG-80',
                'padding': 6,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_household_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Household Code' % company.name,
                'code': 'household.sequence',
                'company_id': company.id,
                'prefix': 'HP-80',
                'padding': 6,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_service_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Service Request Code' % company.name,
                'code': 'farmer.service.request.sequence',
                'company_id': company.id,
                'prefix': 'SR-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_equipment_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Equipment Request Code' % company.name,
                'code': 'farmer.equipment.request.sequence',
                'company_id': company.id,
                'prefix': 'ER-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_expert_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Expert Request Code' % company.name,
                'code': 'farmer.expert.request.sequence',
                'company_id': company.id,
                'prefix': 'EX-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_seedling_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Seedling Request Code' % company.name,
                'code': 'farmer.seedling.request.sequence',
                'company_id': company.id,
                'prefix': 'SLR-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_profile_update_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Profile Update Request Code' % company.name,
                'code': 'farmer.profile.update.request.sequence',
                'company_id': company.id,
                'prefix': 'PUR-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_other_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Other Request Code' % company.name,
                'code': 'farmer.other.request.sequence',
                'company_id': company.id,
                'prefix': 'OR-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_warehouse_location_request_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Warehouse Location Request Code' % company.name,
                'code': 'warehouse.location.sequence',
                'company_id': company.id,
                'prefix': 'SL-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_crop_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Crop Code' % company.name,
                'code': 'farmer.crop.sequence',
                'company_id': company.id,
                'prefix': 'CRO-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_animal_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Animal Code' % company.name,
                'code': 'farmer.animal.sequence',
                'company_id': company.id,
                'prefix': 'ANI-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    def _create_farmer_fish_code_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': '%s Farmer Fish Code' % company.name,
                'code': 'farmer.fish.sequence',
                'company_id': company.id,
                'prefix': 'FI-80',
                'padding': 5,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    @api.model_create_multi
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        payment_orm = self.env['payment.provider']
        payment_providers = payment_orm.sudo().search([('code','in',['esewa','khalti','demo']),('company_id','=',1)])
        models_to_replicate = ['account.account','account.journal']
        fields_to_nullify = ['default_account_id','suspense_account_id','loss_account_id','profit_account_id']



        for comp in res:
            code_names = []
            for provider in payment_providers:
                if provider.code not in code_names:
                    code_names.append(provider.code)
                    provider_copy = provider.copy()
                    provider_copy.company_id = comp
                    provider_copy.website_id = None
                    provider_copy.domain_name = None

                    if hasattr(provider_copy,'khalti_auth_key'):
                        provider_copy.khalti_auth_key = None
                    if hasattr(provider_copy,'merchant_code'):
                        provider_copy.merchant_code = None


            for model in models_to_replicate:
                records = self.env[model].sudo().search([('company_id','=',1)])

                for record in records:
                    record.copy_mode = True
                    new_record = record.copy()
                    if model == 'account.journal':
                        for field in fields_to_nullify:
                            name = new_record.name.split(' - ')
                            new_record['name'] = name[0]
                            new_record[field] = None
                    new_record.company_id = comp
                    new_record.name = new_record.name.split('(')[0]
                    record.copy_mode = False



            if comp.is_local_entity:
                #creting admin user for the company
                user_info={
                    'virtual_login':'admin',
                    'password':'admin',
                    'company_ids':[(4,comp.id)],
                    'company_id':comp.id,
                    'name':comp.name+' admin',
                }
                uid = self.env["res.users"].with_company(comp).create(user_info)
                # Define the names of the access groups you want to assign by default
                default_access_groups = [
                    'farmer.group_admin_access',
                    'farmer.group_all_user_no_access',
                    # 'website.group_website_restricted_editor',
                    'base.group_erp_manager',
                    # 'account.group_account_manager',
                    'sales_team.group_sale_manager',
                    'point_of_sale.group_pos_manager',
                    'stock.group_stock_manager',
                    'hr.group_hr_user',
                    'purchase.group_purchase_manager'
                ]
                access_groups = [ self.env.ref(i) for i in default_access_groups ]
                uid.groups_id = [(4, group.id) for group in access_groups]

                comp._create_farmer_code_sequence()
                comp._create_farmer_group_code_sequence()
                comp._create_household_code_sequence()
                comp._create_farmer_service_request_sequence()
                comp._create_farmer_equipment_request_sequence()
                comp._create_farmer_expert_request_sequence()
                comp._create_farmer_seedling_request_sequence()
                comp._create_farmer_profile_update_request_sequence()
                comp._create_farmer_other_request_sequence()
                comp._create_farmer_warehouse_location_request_sequence()
                comp._create_farmer_crop_code_sequence()
                comp._create_farmer_animal_code_sequence()
                comp._create_farmer_fish_code_sequence()
            elif comp.is_producer_entity:
                temp = self._context['allowed_company_ids'][0]
                temp = self.env['res.company'].search([('id','=',temp)])
                if temp.is_local_entity:
                    comp.parent_id = temp.id
                else:
                    comp.parent_id = temp.parent_id.id

                curr_comp_users = self.env['res.users'].search([('company_id','=',comp.parent_id.id),('groups_id','in',[self.env.ref('farmer.group_surveyor_access').id])])
                for user in curr_comp_users:
                    user.sudo().write({
                        'company_ids' : [(4,comp.id)]
                    })

                producer = self.env['farm.producer'].search([('company_id','=',comp.id)])
                user_info={
                    'login':comp.mobile,
                    'password':comp.mobile,
                    'name':comp.name,
                    'image_1920': producer.image_1920
                }
                uid = self.env["res.users"].with_company(comp).create(user_info)
                default_access_groups = [
                    'farmer.group_producer_farmer_access',
                    'farmer.group_all_user_no_access',
                    # 'website.group_website_restricted_editor',
                    'base.group_erp_manager',
                    'account.group_account_manager',
                    'sales_team.group_sale_manager',
                    'point_of_sale.group_pos_manager',
                    'stock.group_stock_manager',
                    # 'hr.group_hr_user',
                    'purchase.group_purchase_manager'
                ]
                access_groups = [ self.env.ref(i) for i in default_access_groups ]
                uid.sudo().write({
                    "groups_id" : [(4, group.id) for group in access_groups]
                })

                pos_info={
                    'name':comp.name+' shop'
                }
                pos = self.env['pos.config'].with_company(comp).sudo().create(pos_info)
            else:
                pass



        return res