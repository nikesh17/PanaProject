import logging
import pprint
import json
import requests
from odoo import http
from odoo.http import request

import ast
_logger = logging.getLogger(__name__)

class KhaltiController(http.Controller):
    _redirect_url = '/khalti/successful'

    @http.route(
        _redirect_url, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def goto_khalti_payment(self, **data):
        pidx=data['pidx']
        transaction_orm=http.request.env['payment.transaction']
        transaction_item=transaction_orm.sudo().search([('pidx','=',pidx)])
        
        payload={
            "pidx":pidx
        }
        
        response = transaction_item.provider_id._make_khalti_request(payload,mode="lookup")
        if response['status']=='Completed':
            transaction_item._set_done()
        if response['status'] in ['Pending','Initiated']:
            transaction_item._set_pending()
        if response['status']=='Expired':
            transaction_item._set_canceled()

        return request.redirect('/payment/status')
        