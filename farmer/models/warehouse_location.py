from odoo import models,fields,_,api
from odoo.exceptions import ValidationError,UserError
import nepali_datetime

class WarehouseType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'warehouse.type'
    _description = 'warehouse location type'

    name = fields.Char(string=_('Name'))
    name_np = fields.Char(string=_('Name(NEP)'))
    
    def name_get(self):
        result = []
        if self._context["lang"]=='ne_NP':
            for rec in self:
                result.append((rec.id, rec.name_np))
        else:
            for rec in self:
                result.append((rec.id, rec.name))
        return result
        
class WarehousePOC(models.Model):
    _inherit = 'fis.base.model'
    _name = 'warehouse.location.poc'
    _inherits = {'res.users': 'user_id'}

    user_id = fields.Many2one('res.users',store=True, required=True, ondelete='cascade', auto_join=True, index=True, string=_('Related User'), help=' Data of the user',)
    # ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Warehouse ID'), )
    warehouse_id = fields.Many2one("warehouse.location",string=_("Warehouse"))

    @api.model
    def create(self, vals):
        warehouse_id = self.env.context.get('active_id', '0')
        warehouse_obj = self.env['warehouse.location'].search([('id', '=', warehouse_id)])
        vals['login'] = vals['mobile']
        vals['warehouse_id'] = warehouse_obj.id
        poc = super(WarehousePOC, self).create(vals)
        warehouse_obj.write({'poc_id': poc.id})
        return poc

class WarehouseLocationMember(models.Model):
    _inherit = 'fis.base.model'
    _name = 'warehouse.location.member'
    _description= 'Warehouse Location Member'
    
    warehouse_id = fields.Many2one('warehouse.location',string=_("Storage"))
    farmer_id = fields.Many2one('farm.farmer')
    position = fields.Selection([
        ('Member','Member'),
        # ('Chairman/Coordinator','Chairman/Coordinator'),
        # ('Secretary','Secretary'),
        # ('Treasurer','Treasurer'),
    ])
    can_accept_request = fields.Boolean(string=_("Can Accept Request"))

    @api.depends('can_accept_request')
    def _allowed_users_update(self):
        for record in self:
            if record.can_accept_request:
                record.warehouse_id = [(4, record.farmer_id.producer_id.user_id.id)]
            else:
                record.warehouse_id = [(3, record.farmer_id.producer_id.user_id.id)]



class WarehouseStorageRequest(models.Model):
    _inherit = 'fis.base.model'
    _name="warehouse.storage.request"
    _description= 'Warehouse Storage Request'
    # _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']

    warehouse_id = fields.Many2one("warehouse.location",string=_("Storage"))
    allowed_users = fields.Many2many(related="warehouse_id.allowed_users")
    # producer_id = fields.Many2one("farm.producer",string=_("Request Receipient"))
    requested_amount = fields.Float(string=_("Requested Amount"))
    unit_of_measurement = fields.Many2one('uom.uom',string=_('Unit'),domain="[('category_id','=',6)]")

    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    storage_recipient = fields.Many2one('farm.producer',string=_("Request Recipient"),required=True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)


    #only show when storage recipient is selected
    storage_recipient_set = fields.Boolean(store=False,compute="_compute_storage_recipient_details")
    storage_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_storage_recipient_details")
    storage_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_storage_recipient_details")
    storage_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_storage_recipient_details")
    storage_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_storage_recipient_details")
    storage_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_storage_recipient_details")
    storage_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('storage', 'storage')
    ], _("Recipient Gender"),store=True,compute="_compute_storage_recipient_details")

    previous_storage_request_inverse = fields.Many2one('warehouse.storage.request')
    previous_storage_requests = fields.One2many('warehouse.storage.request','previous_storage_request_inverse',compute='_compute_previous_storage_requests')
    storage_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="fish.larva Request State",store=False)

    @api.depends('storage_request_dynamic_state')
    def _compute_previous_storage_requests(self):
        for record in self:
            domain = ['&',
                    ('storage_recipient','=',record.storage_recipient.id),
                    # ('storage_list','in',[rec.id for rec in record.storage_list]),
                    ('id','!=',record._origin.id)]
            if self.storage_request_dynamic_state != 'false':
                domain += [('state', '=', self.storage_request_dynamic_state)]
            temp=[req['id'] for req in self.env['warehouse.storage.request'].search_read(domain,['id'])]
            if temp:
                record.previous_storage_requests = temp
            else:
                record.previous_storage_requests = None


    @api.onchange('storage_recipient')
    def _compute_storage_recipient_details(self):
        for record in self:
            if record.storage_recipient:
                record.storage_recipient_set = True
            record.storage_recipient_name = record.storage_recipient.name
            record.storage_recipient_phone = record.storage_recipient.phone
            record.storage_recipient_mobile = record.storage_recipient.mobile
            record.storage_recipient_vat = record.storage_recipient.vat
            record.storage_recipient_gender = record.storage_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.storage_recipient.id)])
            if len(farmer_id)>0:
                record.storage_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.storage_recipient_farmer_group = None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    curr_user_id = fields.Many2one("res.users",compute="_get_current_uid")

    def approve_request(self):
        if not self.env.user.user_has_groups('farmer.group_user_access') and self.curr_user_id.id not in [i.id for i in self.allowed_users]:
            raise UserError(_("You aren't authrised to confirm this request."))
        self.state = 'Approved'

    def _get_current_uid(self): 
        """ 
        :param self: 
        :return: 
        """ 
        if self.env.context.get('uid', False): 
            self.curr_user_id = self.env.context.get('uid' , False) 
        else: 
            self.curr_user_id = False

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())

class WarehouseLocation (models.Model):
    _inherit = 'fis.base.model'
    _name= 'warehouse.location'
    _description= 'Warehouse Location'
    # _inherits = {"stock.warehouse":"warehouse_id"}

    # warehouse_id = fields.Many2one("stock.warehouse",string=_("Storage"))
    allow_external_stocks = fields.Boolean(string=_("Allow External Stocks"),default=False)
    stock_warehouse_type=fields.Selection([
        ('producer','producer'),
        ('storage','storage'),
        ('other','other'),
    ])
    ref = fields.Char(readonly=1,default=lambda self: _('New'), string=_('Storage Sequence ID'), )
    # name = fields.Char(string=_('Warehouse Name'))
    name = fields.Char(string=_('Name'),required=True)
    code = fields.Char(string=_('Code'),required=True)
    capacity = fields.Float(string=_('Capacity'))
    unit_of_measurement = fields.Many2one('uom.uom',string=_('Unit'),domain="[('category_id','=',6)]")
    warehouse_type = fields.Many2one('warehouse.type',string=_('Storage Type'))
    details = fields.Char(string=_('Details'))
    ownership_type = fields.Selection([
        ('org','Organization Owned'),
        ('comm','Community Owned'),
    ],string=_("Ownership Type"),required=True,default='comm')
    owner_org = fields.Many2one("organization.farmer",string=_("Ogranization"))

    # Address Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))
    
    poc_id = fields.Many2one('warehouse.location.poc', string='POC')
    poc_name = fields.Char(related='poc_id.name', string='POC Name', store=False)
    poc_mobile = fields.Char(related='poc_id.mobile', string='POC Mobile', store=False)
    poc_email = fields.Char(related='poc_id.email', string='POC Email', store=False)

    def action_edit_poc(self):
        warehouse_obj = self.env['warehouse.location'].search([('id', '=', self.id)])
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'warehouse.location.poc',
                'target': 'new',
                'res_id': warehouse_obj.poc_id.id,
            }

    warehouse_location_membership_ids = fields.One2many("warehouse.location.member","warehouse_id",string="Members")
    allowed_users = fields.Many2many("res.users",'allowed_users',compute='_populate_positions',store=True)
    member_users = fields.Many2many("res.users",'member_users',compute='_populate_positions',store=True)


    @api.depends('warehouse_location_membership_ids')
    def _populate_positions(self):
        for record in self:
            record.allowed_users = [(5,)]
            for members in record.warehouse_location_membership_ids:
                record.member_users = [(4, members.farmer_id.producer_id.user_id.id)]
                if members.can_accept_request:
                    members.farmer_id.allowed_warehouses = [(4, record.id)] 
                    record.allowed_users = [(4, members.farmer_id.producer_id.user_id.id)]

    @api.model
    def create(self, vals):
        vals["stock_warehouse_type"]="storage"
        vals['ref'] = self.env['ir.sequence'].next_by_code("warehouse.location.sequence")
        return super(WarehouseLocation, self).create(vals)


    def warehouse_storage_request_window(self):
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'tree,form',
                'view_mode': 'tree,form',
                'res_model': 'warehouse.storage.request',
                'domain':[("warehouse_id","=",self.id)]
            }

    def warehouse_storea_srocks_window(self):
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'tree,form',
                'view_mode': 'tree,form',
                'res_model': 'stock.quant',
                'domain':[("warehouse_id","=",self.id)]
            }