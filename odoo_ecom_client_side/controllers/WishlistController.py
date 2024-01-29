import json
from odoo import http
from odoo.http import request
from . import main


class WishlistController(main.EcomClientController):
    @http.route(
        '/api/v1/wishlist', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_wishlist(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        wishlist_items = http.request.env['product.wishlist'].sudo().search([('partner_id','=',partner.id)])

        wishlist_items_dict = wishlist_items.read(['product_id','pricelist_id','price'])


        for item in wishlist_items_dict:
            product_data = item.pop('product_id')
            item.pop('price')
            item['product'] = self.fetch_single_product(product_data[0])
            item['pricelist_id'] = item.get('pricelist_id')[0]


        
        return json.dumps({'success':True,'data':wishlist_items_dict})

    @http.route(
        '/api/v1/wishlist/add', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def add_wishlist(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        try:
            json_data = json.loads(request.httprequest.data)
        except Exception as e:
            return json.dumps({'success':False,'message':'JSON Body is required'})
        
        partner = self.get_user(uid).partner_id

        for item in json_data:
            product_id = item.get('product_id')
            pricelist_id = item.get('pricelist_id')


            if not product_id or not pricelist_id:
                return json.dumps({'success':False,'message':'Product and Pricelist IDs must be provided'})
            
            record = http.request.env['product.wishlist'].sudo().search([('partner_id','=',partner.id),('product_id','=',product_id)])
            
            if record:
                continue

            try:            
                http.request.env['product.wishlist'].sudo().create({
                    'product_id':product_id,
                    'pricelist_id':pricelist_id,
                    'partner_id':partner.id,
                    'website_id':1
                })
            except Exception as e:
                continue
        
        return json.dumps({'success':True,'message':'Products added to wishlist successfully'})

    @http.route(
        '/api/v1/wishlist/remove', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def remove_wishlist(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        uid = self.validate_user()
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        json_data = json.loads(request.httprequest.data)
        product_ids = json_data.get('product_ids')
        # print(product_ids)

        for product in product_ids:

            try:
                int(product)
            except Exception as e:
                return json.dumps({'success':False,'message':'Provide the details in valid format, Product IDs must be integer'})

        partner = self.get_user(uid).partner_id
        wishlist_items = http.request.env['product.wishlist'].sudo().search([('partner_id','=',partner.id),('product_id','in',product_ids)])

        for item in wishlist_items:
            item.sudo().unlink()

        return json.dumps({'success':True,'message':'Items deleted successfully'})