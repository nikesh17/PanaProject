import json
from odoo import http
from odoo.http import request
from . import main

class CartController(main.EcomClientController): 

    def get_current_cart(self,partner,data=None):
        json_data = {}
        if not data:
            try:
                json_data = json.loads(request.httprequest.data)
                website_id = json_data.get('website_id') 
            except Exception as e:
                return json.dumps({'success':False,'message':'JSON Body is required'})
        else:
            website_id = data.get('wid') 
        if not website_id:
            return json.dumps({'success':False,'message':'Website ID is a required field'})

        cart = None
        cart_orders = http.request.env['sale.order'].sudo().search([('partner_id','=',partner.id),('state','=','draft'),('website_id','=',int(website_id))])
        if cart_orders:
            cart = sorted(cart_orders,key=lambda o:o.id,reverse=True)[0]
        return json_data,website_id,cart



    @http.route(
        '/api/v1/cart', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_cart_items(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        print(self.get_current_cart(partner,data=kw))
        _,__,cart_items = self.get_current_cart(partner,data=kw)

        if not cart_items:
            return json.dumps({'success':False,"message":"This user has no items in the cart"})
        
        cart_data = []

        for line in cart_items.order_line:
            cart_data.append({
                "product_id":line.product_id.id,
                "product_qty":line.product_uom_qty
            })
        return json.dumps({'success':True,'data':cart_data})


    @http.route(
        '/api/v1/cart/add', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def add_cart(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

       
        partner = self.get_user(uid).partner_id

        json_data,website_id,cart_record=self.get_current_cart(partner=partner)
        item = json_data.get('data')

        product_id = item.get('product_id')
        quantity = item.get('quantity') if item.get('quantity') else 1

        print("==============>",cart_record)
        if not product_id:
            return json.dumps({'success':False,'message':'Product and Pricelist IDs must be provided'})
        
        line_id = None
        if cart_record:
            cart_record_lines = cart_record.order_line
            for line in cart_record_lines:
                if product_id == line.product_id.id:
                    line_id = line_id
        else:
            cart_record = http.request.env['sale.order'].sudo().create({
                'partner_id':partner.id,
                'website_id':website_id,
                'state':'draft'
            })


        cart_record._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=quantity,
        )
        return json.dumps({'success':True,'message':'Products added to cart successfully'})


    @http.route(
        '/api/v1/cart/remove', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def remove_cart(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user()
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        json_data,_,cart_record=self.get_current_cart(partner=partner)
        product = json_data.get('product_id')
        


        try:
            product_id = int(product)
            print(cart_record)
            for line in cart_record.order_line:
                print(line)
                if product_id == line.product_id.id:
                    line.unlink()

        except Exception as e:
            return json.dumps({'success':False,'message':'Provide the details in valid format. Please pass product ID as Integer'})



        return json.dumps({'success':True,'message':'Items deleted successfully'})

    @http.route(
        '/api/v1/cart/apply_promo', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def apply_pricelist(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user()
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        json_data,_,cart_record=self.get_current_cart(partner=partner)
        
        promo_code = json_data.get('promo_code')

        if promo_code:        
            promo = http.request.env['product.pricelist'].sudo().search([('code','=',promo_code)])
            if not promo:
                return json.dumps({'success':False,'message':'Sorry, the requested promo does\'nt exist'})
            cart_record._cart_update_pricelist(pricelist_id=promo.id)

        else:
            cart_record._cart_update_pricelist(update_pricelist=True)

        return json.dumps({'success':True,'message':'Promo applied successfully'})
    
    @http.route(
        '/api/v1/cart/select_delivery', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def apply_delivery_charge(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user()
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        json_data,_,cart_record=self.get_current_cart(partner=partner)
        carrier_id = json_data.get('carrier_id')
        DeliveryCarrier = http.request.env['delivery.carrier'].sudo()
        carrier = DeliveryCarrier.browse(carrier_id)
        if carrier:
                res = carrier.rate_shipment(cart_record)
                if res.get('success'):
                    cart_record.set_delivery_line(carrier, res['price'])
                    cart_record.delivery_rating_success = True
                    cart_record.delivery_message = res['warning_message']
                else:
                    cart_record.set_delivery_line(carrier, 0.0)
                    cart_record.delivery_rating_success = False
                    cart_record.delivery_message = res['error_message']
        print(res)

        return json.dumps({'success':True,'message':'Delivery Carrier Applied Successfully','data':{
            'delivery_charge':cart_record.amount_delivery
        }})

        
