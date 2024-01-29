import json
from odoo import http
from odoo.http import request
from . import main


class TransactionController(main.EcomClientController):

    # _transaction_providers = '/api/v1/transaction/providers'
    @http.route(
        '/api/v1/transaction/providers', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_payment_providers(self, **kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        records = http.request.env['payment.provider'].sudo().search([]).read(fields=['id','code'])
        return json.dumps({'success':True,'data':records})


    # _init_transaction = '/api/v1/transaction/init'
    @http.route(
        '/api/v1/transaction/init', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def initialize_transaction(self, **data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        uid = self.validate_user(data)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        
        json_data = json.loads(request.httprequest.data)
        partner = self.get_user(uid).partner_id
        reference = json_data.get('reference')
        provider = json_data.get('provider')
        currency = json_data.get('currency')
        payment_idx = json_data.get('pidx')

        order_id = http.request.env['sale.order'].sudo().search([('name','=',reference)])
        provider_id = http.request.env['payment.provider'].sudo().search([('code','=',provider),('state','in',('enabled','test'))])
        currency_id = http.request.env['res.currency'].sudo().search([('name','=',currency),('active','=',True)])

        if not payment_idx:
            return json.dumps({'success':False,'message':'Payment Transaction ID is not provided'})
        if not partner:
            return json.dumps({"success": False, "message": "Partner not found"})
        if not reference:
            return json.dumps({"success": False, "message": "Reference not provided"})   
        if not provider_id:
            return json.dumps({"success": False, "message": "Provider ID not found"})  
        if not currency_id:
            return json.dumps({"success": False, "message": "Currency ID not found"}) 
        
        partner_id = partner.id

        transaction = http.request.env['payment.transaction'].sudo().create({
                'amount':order_id.amount_total,
                'reference':reference,
                'provider_id':provider_id.id,
                'partner_id':partner_id,
                'currency_id':currency_id.id,
                'state':'pending'
            }
            )
        order = http.request.env['sale.order'].sudo().search([('name','=',reference)])
        order.transaction_ids += transaction
        order.message_post(body=f'Transaction number {transaction.id} has been initiated successfully using {transaction.provider_code} payment method.')
        return json.dumps({'success':True,'data':transaction.read(fields=['id','reference','amount'])})

    # _transaction_status = '/api/v1/transaction/<int:id>'
    @http.route(
        '/api/v1/transaction/<int:id>/status', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_transaction_status(self, **kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        id = kw.get('id')
        record = http.request.env['payment.transaction'].sudo().search([('partner_id','=',partner.id),('id','=',id)])

        if not record:
            return json.dumps({'success':False, 'message':'The transaction for the user does not exist'})
        
        return json.dumps({'success':True,'data':record.read(fields=['id','state'])})



    # _set_transaction_done = '/api/v1/transaction/<int:id>/done'
    @http.route(
        '/api/v1/transaction/<int:id>/done', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def set_transaction_status_done(self,id,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        partner = self.get_user(uid).partner_id
        record = http.request.env['payment.transaction'].sudo().search([('partner_id','=',partner.id),('id','=',id)])

        if not record:
            return json.dumps({'success':False, 'message':'The transaction for the user does not exist'})
        
        try:
            record = record.done()
            reference=record.reference
            order = http.request.env['sale.order'].sudo().search([('name','=',reference)])
            invoice = http.request.env['account.move'].sudo().search([('invoice_origin','=',reference)])
            invoice.api_set_done()
            order.message_post(body=f'Transaction number {record.id} has been paid successfully using {record.provider_code} payment method.')
        except Exception as e:
            return json.dumps({'success':False,'message':'Sorry, your request cannot be fulfilled right now'})
        return json.dumps({'success':True,'data':record.read(fields=['id','state'])})