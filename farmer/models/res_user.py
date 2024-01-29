# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo.http import request
from odoo.exceptions import AccessDenied,ValidationError
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

all_menu = [
    #settings
    'base.menu_action_res_users','base.menu_action_res_company_form','nepali_typing.menu_keyboard',
    #apps
    'base.menu_apps',
    #contacts
    'contacts.res_partner_menu_contacts',
    #link tracker
    'link_tracker.link_tracker_menu_main',
]

hidden_menu=[]

hiding_menu_admin = [
    #settings
    'base.menu_action_res_company_form','nepali_typing.menu_keyboard',
    #contacts
    'contacts.res_partner_menu_contacts',
    #link tracker
    'link_tracker.link_tracker_menu_main',
]
hiding_menu_user = []
hiding_menu_survayor = []
hiding_menu_producer = []
hidden_menu_org_admin = [
    #settings
    'base.menu_action_res_users','base.menu_action_res_company_form','nepali_typing.menu_keyboard',
    #apps
    'base.menu_apps',
    #contacts
    'contacts.res_partner_menu_contacts',
    #link tracker
    'link_tracker.link_tracker_menu_main',
]
hidden_menu_org_user = []

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

super_admin_access_rights = [
    #base
    'base.group_system',
    #farmer
    'farmer.group_super_admin_access',
    #website
    'website.group_website_designer','website.group_website_restricted_editor',
    #accounts
    'account.group_account_manager','account.group_account_user',
    'account.group_account_invoice','account.group_account_readonly',
]

admin_allowed_access_rights = ['FIS/ Surveyor Access', 'FIS/ User Access', 'FIS/ User Admin Access',
                    'FIS/ User Producer Farmer Access', 'FIS/ View Request User Access', 'FIS/ View User Access']

class HideMenuUser(models.Model):
    _inherit = 'res.users'


    hide_menu_ids = fields.Many2many('ir.ui.menu', string="Menu", store=True,
                                     help='Select menu items that needs to be '
                                          'hidden to this user ')
    virtual_login = fields.Char("Login")

     
    show_tax = fields.Boolean("Show tax in invoice", compute='_compute_show_tax')
    show_tax_temp = fields.Boolean("Show tax in invoice",default=True)

    def _compute_show_tax(self):
        for record in self:
            if record.user_has_groups('farmer.group_producer_farmer_access'):
                record.show_tax = record.show_tax_temp
            else:
                record.show_tax = record.company_id.show_tax
        # return temp

    parent_company_id = fields.Many2one("res.company","Associated Company",related='company_id.parent_id')
    
    palika_name = fields.Char(string=_('Palika Name'), compute="_compute_palika_name")

    def _compute_palika_name(self):
        for record in self:
            if record.company_id.is_local_entity:
                record.palika_name = record.company_id.name
            elif record.company_id.parent_id.is_local_entity:
                record.palika_name = record.company_id.parent_id.name
            else:
                record.palika_name = 'Shangrilla Microsystems Private Limited'
    
    palika_id = fields.Many2one('res.company',string=_('Palika'), compute="_compute_palika_id")

    def _compute_palika_id(self):
        for record in self:
            if record.company_id.is_local_entity:
                record.palika_id = record.company_id
            elif record.company_id.parent_id.is_local_entity:
                record.palika_id = record.company_id.parent_id
            else:
                record.palika_id = 1

    palika_receiving_mail = fields.Char(string=_('Receiving Mail'),compute='_compute_palika_receiving_mail')

    def _compute_palika_receiving_mail(self):
        for record in self:
            if record.company_id.is_local_entity:
                record.palika_receiving_mail = record.company_id.email
            elif record.company_id.parent_id.is_local_entity:
                record.palika_receiving_mail = record.company_id.parent_id.email
            else:
                record.palika_receiving_mail = 'noreply@shangrillaLED.com'


    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        hosturl = request.httprequest.environ['HTTP_REFERER'] if request else 'n/a'
        try:
            hosturl = hosturl[hosturl.index('://')+3:hosturl.index('/web')]
        except:
            return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
        print(hosturl)
        new_login = login
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                # temp_user = self.search([('virtual_login', '=', login)], order=self._get_login_order())
                with self._assert_can_auth(user=new_login):
                    user = self.search([('login', '=', login)], order=self._get_login_order())
                    if user:
                        return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
                    user = self.search([('virtual_login', '=', login)], order=self._get_login_order())
                    #cheking if the login info is of superuser (id=2)
                    for u in user:
                        if u.id==2:
                            return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
                        #cheking if the login and virtual_login are same
                        #which means the login shouldn't be generated using the hosturl
                        if u.login==u.virtual_login:
                            return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
                    if not user:
                        user = self.search([('login', '=', login)], order=self._get_login_order())
                        if not user:
                            #cheking if the login info is of superuser (id=2)
                            user = self.search([('virtual_login', '=', login),('id','=',2)], order=self._get_login_order())
                            if not user:
                                raise AccessDenied()
                            return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
                        return super(HideMenuUser,cls)._login(db, login, password, user_agent_env)
                    temp = None
                    active_company = None
                    for u in user:
                        for comp in u.company_ids:
                            for detail in comp.company_detail_ids:
                                if detail.url == hosturl:
                                    temp=u
                                    active_company = comp
                    user=temp
                    if not user:
                        raise AccessDenied()
                    user = user.with_user(user)
                    is_valid_user = False
                    company_ids = [i.id for i in user.company_id]
                    company_ids.sort()
                    i=0
                    for company in user.company_id:
                        new_login += str(company_ids[i])
                        i+=1
                        company_details= company.company_detail_ids
                        for details in company_details:
                            if details.url == hosturl:
                                is_valid_user = True
                                break
                    if not is_valid_user:
                        password="-1hgoajhaj;kl"
        except:
            raise
        request.env.context = dict(request.env.context)
        request.env.context["allowed_company_ids"]=[active_company.id]
        request.env.cr.commit()
        res = super(HideMenuUser,cls)._login(db, new_login, password, user_agent_env)
        return res


    @api.model
    def create(self, vals):
        super_user_access_groups = [self.env.ref(i) for i in super_admin_access_rights]
        super_user_group_ids = [group.id for group in super_user_access_groups]
        for key in vals.keys():
            if 'group' in key:
                id = vals[key]
                # if type(id)!=int and id:
                #     id = int(key[9:])
                if id in super_user_group_ids and not self.env.user.user_has_groups('farmer.group_super_admin_access') and self.env.user.id!=2:
                    raise ValidationError(_("You are not authorised to assign this permission to user"))
        if 'login' in vals.keys():
            return super(HideMenuUser, self).create(vals)
        # if self.env["res.company"].search([('id','=',vals["company_id"])]).is_local_entity:
            # raise ValidationError(_("testing"))
            # if "virtual_login" not in vals.keys() or not vals["virtual_login"]:
            #     raise ValidationError(_("Login info missing."))
            # else:
            #     temp = vals["virtual_login"]
                # try:
                #     temp_company_ids = vals["company_ids"][0][2]
                # except:
                #     temp_company_ids = [vals["company_ids"][0][1]]
                # for id in temp_company_ids:
                #     temp+=str(id)
            # print(vals)
            # temp+=str(vals['company_id'])
            # vals["login"] = temp
            # temp_company_ids = [vals["company_id"]]
            # virtual_login = vals["virtual_login"]
            # users = self.env["res.users"].search_read([('virtual_login','=',virtual_login)],["id"])
            # u_ids = [user["id"] for user in users]
            # if 2 in u_ids:
            #     raise ValidationError(_("Login already in use"))
            # if len(u_ids)>0:
            #     user_objs = self.env["res.users"].search([('id','in',u_ids)])
            #     for user_obj in user_objs:
            #         for c in user_obj.company_ids:
            #             if c.id in temp_company_ids:
            #                 raise ValidationError(_("Login already in use"))
        # else:
        #     vals["login"]=vals["virtual_login"]
        if "virtual_login" in vals.keys():
            vals["login"] = vals["virtual_login"]+str(vals["company_id"])

        self.clear_caches()
        res = super(HideMenuUser, self).create(vals)
        menu_orm=self.env['ir.ui.menu']

        menu_filtered=[self.env.ref(i) for i in all_menu]
        for menu in menu_filtered:
            menu.sudo().write({'restrict_user_ids' : [(3, res.id)]})

        menu_filtered=[self.env.ref(i) for i in hidden_menu]
        menu_array_list=[]
        for menu in menu_filtered:
            menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
            menu_array_list.append(menu.id)
        if res.user_has_groups('farmer.group_super_admin_access'):
            pass
        elif res.user_has_groups('farmer.group_admin_access'):
            menu_filtered=[self.env.ref(i) for i in hiding_menu_admin]
            menu_array_list=[]
            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                menu_array_list.append(menu.id)
        elif res.user_has_groups('farmer.group_user_access'):
            menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_user]
            menu_array_list=[]
            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                menu_array_list.append(menu.id)
        elif res.user_has_groups('farmer.group_surveyor_access'):
            menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_user+hiding_menu_survayor]
            menu_array_list=[]
            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                menu_array_list.append(menu.id)
        if res.user_has_groups('farmer.group_producer_farmer_access'):
            menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_producer]
            menu_array_list=[]
            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                menu_array_list.append(menu.id)
        for group in res.groups_id:
            if group.id == self.env.ref("farmer.group_org_admin_access").id:
                menu_filtered=[self.env.ref(i) for i in hidden_menu_org_admin]
                menu_array_list=[]
                for menu in menu_filtered:
                    menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                    menu_array_list.append(menu.id)
            if group.id == self.env.ref("farmer.group_org_user_access").id:
                menu_filtered=[self.env.ref(i) for i in hidden_menu_org_admin+hidden_menu_org_user]
                menu_array_list=[]
                for menu in menu_filtered:
                    menu.sudo().write({'restrict_user_ids' : [(4, res.id)]})
                    menu_array_list.append(menu.id)
        
        menu_hide_array = vals.get('hide_menu_ids')
        if menu_hide_array is None:
            return res
        # menu_hide_array.pop().append(menu_array_list)
        menu_hide_array[0][-1]=menu_array_list


        return res
        # return super(HideMenuUser, self).(vals)

    def write(self, vals):
        if self.user_has_groups('base.group_public') or self.user_has_groups('base.group_portal') or not self:
            res = super(HideMenuUser,self).write(vals)
            return res
        for record in self:
            super_user_access_groups = [self.env.ref(i) for i in super_admin_access_rights]
            super_user_group_ids = [group.id for group in super_user_access_groups]

            group_change = False
            for key in vals.keys():
                if 'group' in key:
                    group_change = True
                    id = vals[key]
                    if id==True:
                        id = int(key[9:])
                    if id in super_user_group_ids and not record.env.user.user_has_groups('farmer.group_super_admin_access') and record.env.user.id!=2:
                        raise ValidationError(_("You are not authorised to assign this permission to user"))
            res = super(HideMenuUser,record).write(vals)
            # if not group_change:
            #     return res
            menu_filtered=[self.env.ref(i) for i in all_menu]

            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(3, record.id)]})
            menu_filtered=[self.env.ref(i) for i in hidden_menu]
            menu_array_list=[]

            for menu in menu_filtered:
                menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                menu_array_list.append(menu.id)
            for group in record.groups_id:
                if group.id == record.env.ref("farmer.group_super_admin_access").id:
                    pass
                elif group.id == record.env.ref("farmer.group_admin_access").id:
                    menu_filtered=[self.env.ref(i) for i in hiding_menu_admin]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
                elif group.id == record.env.ref("farmer.group_user_access").id:
                    menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_user]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
                elif group.id == record.env.ref("farmer.group_surveyor_access").id:
                    menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_user+hiding_menu_survayor]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
                if group.id == record.env.ref("farmer.group_org_admin_access").id:
                    menu_filtered=[self.env.ref(i) for i in hidden_menu_org_admin]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
                elif group.id == record.env.ref("farmer.group_org_user_access").id:
                    menu_filtered=[self.env.ref(i) for i in hidden_menu_org_admin+hidden_menu_org_user]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
                if group.id == record.env.ref("farmer.group_producer_farmer_access").id:
                    menu_filtered=[self.env.ref(i) for i in hiding_menu_admin+hiding_menu_producer]
                    menu_array_list=[]
                    for menu in menu_filtered:
                        menu.sudo().write({'restrict_user_ids' : [(4, record.id)]})
                        menu_array_list.append(menu.id)
            record.clear_caches()
        return res

