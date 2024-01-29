from odoo import models, fields, _, api

class EcomOrderParent(models.Model):
    _name = 'ecom.order.parent'
    _description = 'Parent Order Table'
    

class EcomTransaction(models.Model):
    _inherit='payment.transaction'

    def done(self):
        return self._set_done()
    

class EcomSaleOrder(models.Model):
    _inherit='sale.order'

    order_parent = fields.Many2one('ecom.order.parent')

    def api_create_order(self,value_list):
        order = super().create(value_list)
        order.state='sale'
        order.invoice_status = 'invoiced'
        return order


    def api_create_invoice(self):
        inv = self.sudo()._create_invoices()
        inv.action_post()
        inv.payment_state='not_paid'
        inv.state='posted'
        inv.move_type='out_invoice'
        inv.message_post(body=f'{inv.name} has been created successfully!')
        return inv
    
class EcomAccountMove(models.Model):
    _inherit='account.move'
    def api_set_done(self):
        self.payment_state='paid'

        return {"status":"successful"}


class CartModel(models.Model):
    _name = 'cart.model'
    _description = 'Cart Items Model for API Clients'
    _sql_constraints = [
        ("product_unique_partner_id",
         "UNIQUE(product_id, partner_id)",
         "Duplicated cart items product for this partner."),
    ]

    partner_id = fields.Many2one('res.partner', string='Owner',required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', help='Pricelist when added')
    quantity = fields.Integer('Product Quantity')


class RatingModel(models.Model):
    _inherit = 'rating.rating'
    files = fields.Many2many('ir.attachment',string="Review Files")


class UserModel(models.Model):
    _inherit = 'res.users'

    def api_login(self,db,login,password, env):
        try:
            uid = self._login(db,login, password,{})
            return uid
        except:
            return False
        








