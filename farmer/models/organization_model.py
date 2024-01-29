from odoo import models, fields,api, _
import nepali_datetime
from odoo.exceptions import ValidationError

class FiscalYear(models.Model):
    _inherit = 'fis.base.model'
    _name = 'fiscal.year'
    _rec_name = 'fiscal_year'

    fiscal_year = fields.Char(string=_('Fiscal Year'))



class OrganizationType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'organization.type'
    _rec_name = 'type'

    type = fields.Char(string=_('Type'))


class OrganizationNature(models.Model):
    _inherit = 'fis.base.model'
    _name = 'organization.nature'
    _rec_name = 'nature'

    nature = fields.Char(string=_('Nature'))


class OrgClosingReason(models.Model):
    _inherit = 'fis.base.model'
    _name = 'organization.closing.reason'
    _rec_name = 'reason'

    reason = fields.Char(string=_('Reason'))

all_groups = [
    #accounts
    'account.group_account_manager','account.group_account_user',
    'account.group_account_invoice','account.group_account_readonly',
    #sales
    'sales_team.group_sale_manager','sales_team.group_sale_salesman_all_leads',
    'sales_team.group_sale_salesman',
    #pos
    'point_of_sale.group_pos_manager','point_of_sale.group_pos_user',
    #website
    'website.group_website_designer','website.group_website_restricted_editor',
    #Project
    'project.group_project_manager','project.group_project_user',
    #inventory
    'stock.group_stock_manager','stock.group_stock_user',
    #survey
    'survey.group_survey_manager','survey.group_survey_user',
    #employees
    'hr.group_hr_manager','hr.group_hr_user',
    #email marketing
    'mass_mailing.group_mass_mailing_user',
    #purchase
    'purchase.group_purchase_manager','purchase.group_purchase_user',
]

class OrgMembers(models.Model):
    _name="organization.member"
    _inherits = { 'res.users' : 'user_id' }

    user_id = fields.Many2one('res.users',string=_('Users'))
    postion = fields.Selection([
        ('Administrator','Administrator'),
        ('Propwriter','Propwriter'),
        ('User','User'),
        ('Accountant','Accountant'),
    ],string=_("Position"),required=True)
    organization_id = fields.Many2one("organization.farmer")
    can_accept_request = fields.Boolean(string=_("Can Accept Request"))

    @api.constrains('postion')
    def _single_admin(self):
        for record in self:
            other_records = self.env['organization.member'].search([('id','!=',record.id),('postion','=',record.postion),('organization_id','=',record.organization_id.id),('postion','=','Administrator')])
            if other_records:
                raise ValidationError(_(record.postion+" is already filled for this Organization."))


    @api.model
    def create(self, vals_list):
        if 'mobile' not in vals_list or not vals_list['mobile']:
            raise ValidationError('Mobile Number is required for Organization Members')

        vals_list['login'] = vals_list['mobile']
        vals_list['password'] = vals_list['mobile']
        vals_list['company_id'] = self.env["organization.farmer"].search([('id','=',vals_list['organization_id'])]).company_id.id
        vals_list['company_ids'] = [(4,self.env["organization.farmer"].search([('id','=',vals_list['organization_id'])]).company_id.id)]
        user = super(OrgMembers, self).create(vals_list)
        # Define the names of the access groups you want to assign by default
        if user.postion=='Propwriter':
            default_access_groups = ['farmer.group_org_user_access','base.group_erp_manager','farmer.group_all_user_no_access']
        elif user.postion=='Administrator':
            default_access_groups = ['farmer.group_org_admin_access','base.group_erp_manager','point_of_sale.group_pos_manager','account.group_account_manager','farmer.group_all_user_no_access','hr.group_hr_user','purchase.group_purchase_manager']
        elif user.postion=='User':
            default_access_groups = ['farmer.group_org_user_access','base.group_erp_manager','point_of_sale.group_pos_user','farmer.group_all_user_no_access']
        elif user.postion=='Accountant':
            default_access_groups = ['farmer.group_org_user_access','base.group_erp_manager','account.group_account_user','farmer.group_all_user_no_access']
        # Find the access groups by name
        access_groups = [ self.env.ref(i) for i in default_access_groups ]

        remove_access_groups = [ self.env.ref(i) for i in all_groups]
        print(remove_access_groups)
        # Assign the user to the found access groups
        user.write({'groups_id': [(3, group.id) for group in remove_access_groups]})
        user.write({'groups_id': [(4, group.id) for group in access_groups]})
        return user

class Organization(models.Model):
    _name = "organization.farmer"
    _description = "Organization Farmer"
    _inherits = {'res.company': 'company_id'}


    # Relational Fields
    # partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
    #                              string='Related Partner', help='Partner-related data of the user',)

    company_id = fields.Many2one('res.company',string=_('Organization'))
    type = fields.Many2one('organization.type',string=_('Organization Type'))
    nature = fields.Many2one('organization.nature',string=_('Organization Nature'))
    registration_number = fields.Char(string=_('Registration Number'))
    registration_date = fields.Date(string=_('Registration Date'),compute="_obtain_registration_date_ad")
    registration_date_bs = fields.Char(string=_('Registration Date(B.S.)'),required=False)
    registration_district = fields.Many2one('location.district',string=_('Registration District'))

    #organization functional details
    start_date = fields.Date(string=_('Start Date'),compute="_obtain_start_date_ad")
    start_date_bs = fields.Char(string=_('Start Date(B.S.)'),required=False)

    close_date = fields.Date(string=_('Close Date'),compute="_obtain_close_date_ad")
    close_date_bs = fields.Char(string=_('Close Date(B.S.)'),required=False)

    recent_paid_tax_year = fields.Many2one('fiscal.year',string=_('Recent Tax Paid Year'))
    yearly_transaction = fields.Float(string=_('Yearly Transaction'))

    type_of_service = fields.Selection([
        ('Shop','Shop'),
        ('Restaurant','Restaurant'),
    ],string=_("Type of Service"),required=True)

    #local regsitration details
    local_reg_number = fields.Char(string=_('VDC/Municipality Registration Number'))
    local_reg_date_bs = fields.Char(string=_("Registation Date(B.S.)"))
    local_reg_date = fields.Date(string=_("Registation Date"),compute="_obtain_local_registration_date_ad")
    members = fields.One2many("organization.member",'organization_id',string=_("Members"))
    storage_location = fields.One2many("warehouse.location",'owner_org',string=_("Members"))

    @api.constrains('members','storage_location')
    def _allow_org_members_storage_access(self):
        for record in self:
            print(record)
            for str_loc in record.storage_location:
                str_loc.allowed_users = [(5,)]
                for mem in record.members:
                    str_loc.member_users = [(4,mem.user_id.id)]
                    if mem.can_accept_request:
                        str_loc.allowed_users = [(4,mem.user_id.id)]

    @api.depends('local_reg_date_bs')
    def _obtain_local_registration_date_ad(self):
        for record in self:
            if record.local_reg_date_bs:
                record.local_reg_date = nepali_datetime.datetime.strptime(record.local_reg_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.local_reg_date=None

    @api.depends('start_date_bs')
    def _obtain_start_date_ad(self):
        for record in self:
            if record.start_date_bs:
                record.start_date = nepali_datetime.datetime.strptime(record.start_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.start_date=None

    @api.depends('close_date_bs')
    def _obtain_close_date_ad(self):
        for record in self:
            if record.close_date_bs:
                record.close_date = nepali_datetime.datetime.strptime(record.close_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.close_date=None

    @api.depends('registration_date_bs')
    def _obtain_registration_date_ad(self):
        for record in self:
            record.registration_date = nepali_datetime.datetime.strptime(record.registration_date_bs, '%Y-%m-%d').to_datetime_date()

    pan_number = fields.Char(string=_('Pan Number'))
    #location fields Many2one
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    # photo = fields.Binary(string=_('Photo'))

    #organization registation related fields
    
    @api.constrains('number')
    def action_save(self):
        # self.ensure_one()
        self.write({})
        return True

    def action_cancel(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}


    @api.model
    def create(self, vals):
        vals['is_local_entity'] = False
        print(self._context.get('allowed_company_ids'))
        vals['parent_id'] = self._context.get('allowed_company_ids')[0]
        print(vals)
        res = super(Organization, self).create(vals)
        if res.type_of_service=='Shop':
            pos_info={
                'name':res.name+' shop'
            }
        elif res.type_of_service=='Restaurant':
            pos_info={
                'name':res.name+' restaurant',
                'module_pos_restaurant': True
            }
        pos = self.env['pos.config'].with_company(res.company_id).sudo().create(pos_info)
        return res


