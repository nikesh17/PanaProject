import json
from odoo import http
from . import main


class InvoiceController(main.EcomClientController):
   

    # For Invoice
    @http.route(
        '/api/v1/invoices', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_invoices(self, **kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        partner = self.get_user(uid).partner_id
        if not partner:
            return json.dumps({'success':False,'message':'This user does not exist'})
        records = http.request.env['account.move'].sudo().search([('partner_id','=',partner.id)])
        if not records:
            return json.dumps({
            "success":False,
            "message": "This user does not have any invoice records"
        })
        return json.dumps({'sucess':True,'data':records.read(fields=['id','partner_id','payment_state','state','invoice_origin','name'])})



    # For Single Invoice
    @http.route(
        '/api/v1/invoices/<int:invoice_id>', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_invoice(self, **kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        single_invoice_id = kw.get('invoice_id')
        uid = self.validate_user(kw)
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        partner = self.get_user(uid).partner_id
        if not partner:
            return json.dumps({'success':False,'message':'This user does not exist'})
        records = http.request.env['account.move'].sudo().search([('partner_id','=',partner.id),('id','=',single_invoice_id)])

        if not records:
            return json.dumps({'success':False,'message':'Sorry, cannot find the invoice with the provided id for the user'})
        return json.dumps({'success':True,'message':records.read(fields=['id','partner_id','payment_state','state','invoice_origin','name'])})