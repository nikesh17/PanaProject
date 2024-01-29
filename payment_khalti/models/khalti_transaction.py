from odoo.exceptions import ValidationError
from odoo import api, fields, models
from datetime import datetime
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class KhaltiTransaction(models.Model):
    _inherit = 'payment.transaction'   
    pidx=fields.Char('pidx')

    @api.constrains('state')
    def _check_state_authorized_supported(self):
        pass
    

    @api.model_create_multi
    def create(self, values_list):
        tsx = super().create(values_list)
        tsx.state='pending'
        return tsx
    
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        
        if self.provider_id.code != 'khalti':
            return res
        
        
        payload = {
            'amount': int(self.amount*100),
            'return_url':f'{self.provider_id.domain_name}/khalti/successful',
            'website_url':f'{self.provider_id.domain_name}/',
            'purchase_order_name': f"Ref: {self.reference}",
            'purchase_order_id': self.reference,
        }
        
        response = self.provider_id._make_khalti_request(payload)
        payment_url = response['payment_url']
        pidx=response['pidx']
        self.pidx=pidx
        
        return {
            'payment_url':payment_url,
            'pidx':pidx
        }
    
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Adyen data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if inconsistent data were received
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        return tx
    
    def action_khalti_set_done(self):
        """ Set the state of the khalti transaction to 'done'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return

        self._set_done()

    def action_khalti_set_pending(self):
        """ Set the state of the khalti transaction to 'pending'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return

        self._set_pending()

    def action_khalti_set_auth(self):
        """ Set the state of the khalti transaction to 'authorized'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return
        self.action_khalti_set_draft()
        self._set_authorized()


    def action_khalti_set_canceled(self):
        """ Set the state of the khalti transaction to 'cancel'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return

        self._set_canceled()

    def action_khalti_set_error(self):
        """ Set the state of the khalti transaction to 'error'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return

        self._set_error("Error Has Occured Registering This Payment")

    def action_khalti_set_draft(self):
        """ Set the state of the khalti transaction to 'error'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'khalti':
            return

        self.state='draft'
        

        
        
        
    
