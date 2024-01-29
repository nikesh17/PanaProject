import json
from odoo import http
from odoo.http import request
from . import main

class OrderController(main.EcomClientController):

    def read_order(self,records):
        records_data_dict = records.read(fields=['id','invoice_status','state','name','amount_total','amount_untaxed','amount_tax'])

        for record in records_data_dict:
            record['tracking_id'] = record['name']
            record['products'] = []

            del record['name']
            sale_order_line = http.request.env['sale.order.line'].sudo().search([('order_id','=',record['id'])])

            for order_line in sale_order_line:
                record['products'].append({
                    'product_id':order_line.product_id.id,
                    'name':order_line.name,
                    'product_quantity':order_line.product_uom_qty,
                    'product_uom':order_line.product_uom.name,
                    'price_total':order_line.price_total
                })
        return records_data_dict


    @http.route(
        '/api/v1/orders', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_orders(self,**data):     
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        user_id = self.validate_user(data)
        if not user_id:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        partner = self.get_user(user_id).partner_id
        if not partner:
            return json.dumps({'success':False,'message':'Sorry, the user does not exist.'})
        records = http.request.env['sale.order'].sudo().search([('partner_id','=',partner.id)])

        if not records:
            return json.dumps({
            "success":False,
            "message": "This user does not have any order records"
        })

        records_data_dict = self.read_order(records)            

        return json.dumps({
            "success":True,
            "data": records_data_dict
        })



    @http.route(
        '/api/v1/orders', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def create_order(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        user_id = self.validate_user(data)
        
        try:
            json_data = json.loads(request.httprequest.data)
            price_list = json_data.get("price_list_id")
            delivery_option = json_data.get("delivery_option_id")
            order_list = json_data.get('order_data')
            partner_id = json_data.get('partner_id')
        except Exception as e:
            return json.dumps({'success':False,'message':'Wrong data format provided'})
        
        
        price_list = http.request.env['product.pricelist'].sudo().search([('id','=',price_list)])
        delivery_option = http.request.env['delivery.carrier'].sudo().search([('id','=',delivery_option)])

        if not price_list:
            return json.dumps({'success':False,'message':'Price list ID is required'})
    
        if not delivery_option:
            return json.dumps({'success':False,'message':'Delivery Option ID is required'})

        if not user_id:
            if not partner_id:
                return json.dumps({'success':False,'message':'You must provide partner_id for guest user\'s order'})
            # partner = http.request.env['res.partner'].sudo().search([('id','=',partner_id)])
            create_data = [{'partner_id': partner_id,'state':'draft','invoice_status':'invoiced','order_line': []}]
        else:
            user = self.get_user(user_id)
            create_data = [{'partner_id': user.partner_id.id, 'company_id':user.company_id.id,'state':'draft','invoice_status':'invoiced','order_line': []}]

        for data in order_list:
            create_data[0]['order_line'].append((0,0,{'product_id':data.get('product_id'),'product_uom_qty':data.get('product_qty')}))

        order_orm = http.request.env['sale.order']
        order = order_orm.sudo().api_create_order(create_data)
    
        return json.dumps({'success':True,"data":order.read(fields=['id','invoice_status','state','name','amount_total','amount_untaxed','amount_tax'])})


    @http.route(
        '/api/v1/orders/<int:id>', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_specific_order(self,id,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        user_id = self.validate_user(data)
        if not user_id:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        partner = self.get_user(user_id).partner_id
        if not partner:
            return json.dumps({'success':False,'message':'Sorry, the user does not exist.'})

        order = http.request.env['sale.order'].sudo().search([('partner_id','=',partner.id),('id','=',id)])
        if order:
            return json.dumps({'success':True,'data':order.read(fields=['id','invoice_status','state','name','amount_total','amount_untaxed','amount_tax'])})
        else:
            return json.dumps({"status":False,'message':"Sorry, this user does not have the requested order"})