import logging
import pprint
import json
import requests
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers import main as PaymentController
from odoo.addons.portal.controllers import portal as PortalController
from odoo.addons.payment import utils as payment_utils


import ast
_logger = logging.getLogger(__name__)

class EsewaController(PortalController.CustomerPortal):
    _redirect_url_success = '/esewa/successful'
    _redirect_url_failure = '/esewa/failure'

    @http.route(
        _redirect_url_success, type='http', auth='public', methods=['GET'], csrf=False, save_session=True
    )
    def successful_esewa_payment(self, **data):
        order=data['oid'].split('-')[0]
        esewa_ref=data['refId']
        url = http.request.httprequest.base_url.split('/')[2]
        transaction_orm=http.request.env['payment.transaction']
        payment_orm=http.request.env['payment.provider']
        transaction_item=transaction_orm.sudo().search([('reference','ilike',f'%{order}%')])
        order_item=http.request.env['sale.order'].sudo().search([('name','ilike',f'%{order}%')])
        provider_item=payment_orm.sudo().search([('code','=','esewa'),('domain_name','like',f'%{url}%')])
        transaction_item.ref_id=esewa_ref
        payload={
            "pid":order,
            'rid':esewa_ref,
            'amt':data['amt'],
            'scd':provider_item.merchant_code
            
        }
        print(payload,http.request.httprequest.base_url)

        response = requests.post('https://uat.esewa.com.np/epay/transrec', data=payload)

        if 'Success' in response.content.decode():

            transaction_item._set_done()
 
        else:
            transaction_item._set_pending()

        return request.redirect('/payment/status')

    @http.route(
        _redirect_url_failure, type='http', auth='public', methods=['GET'], csrf=False, save_session=True
    )
    def failure_esewa_payment(self, **data):
        return request.redirect('/payment/status')
        
class PaymentPortanController(PaymentController.WebsiteSale):
    def _get_express_shop_payment_values(self, order, **kwargs):
        logged_in = not request.website.is_public_user()
        providers_sudo = request.env['payment.provider'].sudo().search([('website_id','=',request.website.id)])
        fees_by_provider = {
            p_sudo: p_sudo._compute_fees(
                order.amount_total, order.currency_id, order.partner_id.country_id
            ) for p_sudo in providers_sudo.filtered('fees_active')
        }
        return {
            # Payment express form values
            'providers_sudo': providers_sudo,
            'fees_by_provider': fees_by_provider,
            'amount': order.amount_total,
            'minor_amount': payment_utils.to_minor_currency_units(
               order.amount_total, order.currency_id
            ),
            'merchant_name': request.website.name,
            'currency': order.currency_id,
            'partner_id': order.partner_id.id if logged_in else -1,
            'payment_access_token': order._portal_ensure_token(),
            'transaction_route': f'/shop/payment/transaction/{order.id}',
            'express_checkout_route': self._express_checkout_route,
            'landing_route': '/shop/payment/validate',
        }

    def _get_shop_payment_values(self, order, **kwargs):
        logged_in = not request.env.user._is_public()
        providers_sudo = request.env['payment.provider'].sudo().search([('website_id','=',request.website.id)])
        tokens = request.env['payment.token'].search(
            [('provider_id', 'in', providers_sudo.ids), ('partner_id', '=', order.partner_id.id)]
        ) if logged_in else request.env['payment.token']
        fees_by_provider = {
            p_sudo: p_sudo._compute_fees(
                order.amount_total, order.currency_id, order.partner_id.country_id
            ) for p_sudo in providers_sudo.filtered('fees_active')
        }
        return {
            'website_sale_order': order,
            'errors': [],
            'partner': order.partner_invoice_id,
            'order': order,
            'payment_action_id': request.env.ref('payment.action_payment_provider').id,
            # Payment form common (checkout and manage) values
            'providers': providers_sudo,
            'tokens': tokens,
            'fees_by_provider': fees_by_provider,
            'show_tokenize_input': PaymentController.PaymentPortal._compute_show_tokenize_input_mapping(
                providers_sudo, logged_in=logged_in, sale_order_id=order.id
            ),
            'amount': order.amount_total,
            'currency': order.currency_id,
            'partner_id': order.partner_id.id,
            'access_token': order._portal_ensure_token(),
            'transaction_route': f'/shop/payment/transaction/{order.id}',
            'landing_route': '/shop/payment/validate',
        }
