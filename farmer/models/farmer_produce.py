from odoo import models, fields, _, api
import base64
from odoo.exceptions import UserError, ValidationError
import nepali_datetime
from odoo.tools.float_utils import float_compare, float_is_zero

class FarmerProduceProduction(models.Model):
    _name = 'farmer.produce.production'
    _description = 'Farmer Produce Production'
    _inherits = {'stock.quant':'stock_quant_id'}

    
    # name = fields.Char(string=_('Farmer Produce Production'))
    farmer_production_ids = fields.Many2one("farm.produce","Product")
    product_template_id = fields.Many2one(related="farmer_production_ids.product_id", string="Product Template")
    product_variants = fields.Many2one("product.product", string="Variants",
                                       domain="[('product_tmpl_id', '=', product_template_id)]")
    producer_id = fields.Many2one("farm.producer","Producer",compute='_get_producer_id')
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))

    parent_company_id = fields.Many2one("res.company","Associated Company",related='company_id.parent_id')

    @api.depends('farmer_id','farmer_group_id')
    def _get_producer_id(self):
        for record in self:
            if record.farmer_id:
                record.producer_id = record.farmer_id.producer_id.id
            elif record.farmer_group_id:
                record.producer_id = record.farmer_group_id.producer_id.id

    @api.model
    def create(self, vals):
        produce_id = vals.get('farmer_production_ids')
        variant_id = vals.get('product_variants')
        quantity = vals.get('inventory_quantity')
        if produce_id:
            farmer_produce = self.env['farm.produce'].browse(produce_id)
            product_id = False
            if not vals.get('product_variants'):
                product_id = farmer_produce.product_id.product_variant_ids[:1].id
            else:
                product_id = vals.get('product_variants')
            vals['product_id'] = product_id
            farmer_id = vals.get('farmer_id')
            producer = self.env['farm.farmer'].search([('id', '=', farmer_id)], limit=1)
            if producer:
                producer_id = producer.producer_id.id
                # location_name = 'FA0'+str(producer.id) + 'Incoming Location'
                location_name = 'Incoming Location'
                location = self.env['stock.location'].search([('complete_name', '=ilike', location_name)], limit=1)
                if location:
                    vals['location_id'] = location.id
                    vals['quantity'] = quantity

        return super(FarmerProduceProduction, self).create(vals)


    
class FarmerSellProducts(models.Model):
    _name = 'farmer.sell.products'
    _description = 'Farmer Sell Products'

    # Existing fields
    farmer_sell_ids = fields.Many2one("farm.produce", "Product Sell")
    product_template_id = fields.Many2one(related="farmer_sell_ids.product_id", string="Product Template")
    product_variants = fields.Many2one("product.product", string="Variants",
                                       domain="[('product_tmpl_id', '=', product_template_id)]")
    location_id = fields.Many2one("stock.location", "From")
    location_dest_id = fields.Many2one("stock.location", "To")
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    stock_picking_id = fields.Many2one("stock.picking", "Picking Id")
    quantity_to_transfer = fields.Integer("Quantity")
    transfer_done = fields.Boolean(string="Transfer Done", default=False)

    def _get_default_company(self):
        if "allowed_company_ids" in dict(self.env.context).keys():
            res = self.env.context["allowed_company_ids"][0]
        else:
            res = 1
        res = self.env["res.company"].search([('id','=',res)])[0]
        return res
    company_id = fields.Many2one("res.company","Associated Company",default=_get_default_company)
    parent_company_id = fields.Many2one("res.company","Associated Company",related='company_id.parent_id')
    # Existing methods

    def transfer_product(self):
        producer = self.env['farm.farmer'].search([('id', '=', self.farmer_id.id)], limit=1)
        if producer:
            producer_id = producer.producer_id.id
            # location_name = 'FA0' + str(producer_id) + '/Incoming Location'
            location_name = 'Incoming Location'
            location = self.env['stock.location'].search([('complete_name', '=ilike', location_name)], limit=1)
            if location:
                self.location_id = location.id
            # location_name2 = 'FA0' + str(producer_id) + '/Outgoing Location'
            location_name2 = str(producer.name)[:5]+'/Stock'
            location2 = self.env['stock.location'].search([('complete_name', '=ilike', location_name2)], limit=1)
            if location2:
                self.location_dest_id = location2.id
        
        if not self.transfer_done:
            # Create a stock picking record
            picking_type_id = self.env['stock.picking.type'].search([('name', '=', 'Internal Transfers')], limit=1)
            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
            })

            # Create a stock move to transfer the product
            stock_move = self.env['stock.move'].create({
                'name': 'Stock Transfer',
                'product_id': self.product_variants.id,
                'product_uom_qty': self.quantity_to_transfer,
                'quantity_done': self.quantity_to_transfer,
                'product_uom': self.product_variants.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': picking.id,
                'state': 'draft'
            })

            stock_move._action_confirm()
            stock_move._action_done()

            # Assign the picking ID to the current record
            self.stock_picking_id = picking.id

            # Set the flag to True after the transfer is done
            self.transfer_done = True

            # Commit the changes to the database
            self._cr.commit()

    @api.model
    def create(self, vals):
        res = super(FarmerSellProducts, self).create(vals)
        res.transfer_product()
        return res
    
        
        
#Produce Model
class Produce(models.Model):
    _name = 'farm.produce'
    _description = 'Farm Produce'
    _rec_name = 'name'
    _inherits = {'product.template':'product_id'}
    
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
        
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    household_id = fields.Many2one('farm.household')
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    producer_id = fields.Many2one("farm.producer","Producer",compute='_get_producer_id')
    farmer_produce_production_ids = fields.One2many("farmer.produce.production","farmer_production_ids", string="Farmer Producer Production")
    farmer_sell_products_ids = fields.One2many("farmer.sell.products","farmer_sell_ids", string="Farmer Sell Products")
    # name = fields.Char("Name",compute="compute_name")


    product_id = fields.Many2one('product.template', string=_("Product"))

    @api.depends('farmer_id','farmer_group_id')
    def _get_producer_id(self):
        for record in self:
            if record.farmer_id:
                record.producer_id = record.farmer_id.producer_id.id
            elif record.farmer_group_id:
                record.producer_id = record.farmer_group_id.producer_id.id

    
    # @api.model
    # def create(self, vals):
    #         vals['active'] = False
    #         return super(Produce, self).create(vals)
    
#Fish Type Model
class FishType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'fish.type'
    _description = 'Fish Types'

    name = fields.Char(string=_('Fish Type'))

#Fish Produce Model
class Fish(models.Model):
    _inherit = 'fis.base.model'
    _name = 'farmer.fish'
    _description = 'Fish Information'
    _inherits = {'farm.produce':'produce_id'}

    produce_id  = fields.Many2one('farm.produce',"Produce")
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    fish_types = fields.Many2one('fish.type', string=_('Fish Types'))
    pond_area = fields.Float(string=_('Pond Area'), required=True)
    production_date = fields.Char(string=_('Production Date'))
    baby_fish_release_date = fields.Char(string=_('Release Date'))
    baby_fish_source = fields.Char(string=_('Source'), required=True)
    xchg = fields.Many2one('local.production',string=_('Fields For Exchanging'))
    is_sellable = fields.Boolean(string=_("Is Sellable"))
    is_variant = fields.Boolean(string=_("Is Variant"))

    # name = fields.Char("Household Production")
    unlister_category = fields.Char("Unlisted Category")
    quantity = fields.Float("Quantity")
    fish_purpose = fields.Many2one('animal.purpose', string= _('Animal Purpose'))
    production_frequency = fields.Selection([
        ('day','day'),
        ('week','week'),
        ('month','month'),
        ('year','year'),
    ],string="Per")

    delete_request=fields.Boolean(default=False)
    

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

    @api.model
    def create(self, vals):
            return super(Fish, self).create(vals)


#Produce Crop Name model
class CropName(models.Model):
    _inherit = 'fis.base.model'
    _name = 'crop.name'
    _description = 'Crop Name'

    name = fields.Char(string=_('Crop Name'))

#Produce Crop Type Model
class CropType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'crop.type'
    _description = 'Crop Types'

    crop_name = fields.Many2one('crop.name', string=_("Crop Name"))
    name = fields.Char(string=_('Crop Type'))

#Produce Crop Model
class Crop(models.Model):
    _inherit = 'fis.base.model'
    _name = 'farmer.crop'
    _description = 'Crop Information'
    _inherits = {'farm.produce':'produce_id'}

    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    crop_name = fields.Many2one('crop.name', string=_('Crop Name'), required=True)
    crops_types = fields.Many2one('crop.type', string=_('Crop Type'), required=True)
    area = fields.Float(string=_('Area'), required=False)
    # produce_id  = fields.Many2one('farm.produce',"Produce")
    xchg = fields.Many2one('local.production',string=_('Fields For Exchanging'))
    production_category = fields.Many2one("local.production.category",string="Category")
    is_sellable = fields.Boolean(string=_("Is Sellable"))
    is_variant = fields.Boolean(string=_("Is Variant"))

    # name = fields.Char("Household Production")
    unlister_category = fields.Char("Unlisted Category")
    quantity = fields.Float("Quantity")
    production_frequency = fields.Selection([
        ('day','day'),
        ('week','week'),
        ('month','month'),
        ('year','year'),
    ],string="Per")

    delete_request=fields.Boolean(default=False)
    

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

    @api.model
    def create(self, vals):
            return super(Crop, self).create(vals)

#Local Production Category Model
class LoacalProductionCategory(models.Model):
    _inherit = 'fis.base.model'
    _name = 'local.production.category'
    _description = 'Local Production Category'

    name = fields.Char(string=_('Local Production Category'))

#Local Production type Model
class LoacalProductionType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'local.production.type'
    _description = 'Local Production Type'

    parent_id = fields.Many2one("local.production.category",string=_('Local Production Category'))
    name = fields.Char(string=_('Local Production Type'))




#Local Producer Model
class LocalProduction(models.Model):
    _inherit = 'fis.base.model'
    _name = 'local.production'
    _description = 'Local production'
    _inherits = {'farm.produce':'produce_id'}

    # produce_id  = fields.Many2one('farm.produce',"Produce")
    xchg = fields.Many2one('local.production',string=_('Fields For Exchanging'))
    production_category = fields.Many2one("local.production.category",string="Category")
    production_type = fields.Many2one("local.production.type",string="Type")
    is_sellable = fields.Boolean(string=_("Is Sellable"))
    is_variant = fields.Boolean(string=_("Is Variant"))
    is_seed = fields.Boolean(string=_('Is seed'))

    # name = fields.Char("Household Production")
    unlister_category = fields.Char("Unlisted Category")
    quantity = fields.Float("Quantity")
    area = fields.Float("Area")
    # production_qty = fields.Float("Production Quantity")
    count = fields.Integer("Count")
    production_frequency = fields.Selection([
        ('day','day'),
        ('week','week'),
        ('month','month'),
        ('year','year'),
    ],string="Per")

    delete_request=fields.Boolean(default=False)
    

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

    @api.model
    def create(self, vals):
            return super(LocalProduction, self).create(vals)
    


    

#Produce Animal Name Model s
class AnimalName(models.Model):
    _inherit = 'fis.base.model'
    _name = 'animal.name'
    _description = 'Animal Name'

    name = fields.Char(string=_('Animal Name'))

#Produce Animal Type Model
class AnimalType(models.Model):
    _inherit = 'fis.base.model'
    _name = 'animal.type'
    _description = 'Animal Types'
    _rec_name = "name"

    animal_name = fields.Many2one('animal.name', string=_('Animal Name'))
    name = fields.Char(string=_('Animal Type'))

#Produce Animal Purpose Model
class AnimalPurpose(models.Model):
    _inherit = 'fis.base.model'
    _name = 'animal.purpose'
    _description = 'Animal Purpose'

    name = fields.Char(string=_('Animal Purpose'))

#Produce Animal Model
class Animal(models.Model):
    _inherit = 'fis.base.model'
    _name = 'farmer.animal'
    _description = 'Farmer animals  Information'
    _inherits = {'farm.produce':'produce_id'}

    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    animal_name = fields.Many2one('animal.name', string=_('Animal Name'))
    animals_types = fields.Many2one('animal.type', string=_('Animal Type'))
    animal_purpose = fields.Many2one('animal.purpose', string= _('Animal Purpose'))
    xchg = fields.Many2one('local.production',string=_('Fields For Exchanging'))
    production_category = fields.Many2one("local.production.category",string="Category")
    is_sellable = fields.Boolean(string=_("Is Sellable"))
    is_variant = fields.Boolean(string=_("Is Variant"))


    # name = fields.Char("Household Production")
    unlister_category = fields.Char("Unlisted Category")
    quantity = fields.Float("Count")
    is_milk_producer = fields.Boolean(string=_("Is Milk Producer"))
    is_egg_producer = fields.Boolean(string=_("Is Egg Producer"))

    daily_milk_production = fields.Float(string=_("Daily Milk Producetion"))
    milk_production_month = fields.Integer(string=_("Milk Producetion Month Count"))

    annual_egg_production = fields.Integer(string=_("Annual Egg Producetion"))
    annual_egg_production_sell = fields.Integer(string=_("Annual Egg Producetion For sale"))

    production_frequency = fields.Selection([
        ('day','day'),
        ('week','week'),
        ('month','month'),
        ('year','year'),
    ],string="Per")

    delete_request=fields.Boolean(default=False)
    

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

    @api.model
    def create(self, vals):
            return super(Animal, self).create(vals)
