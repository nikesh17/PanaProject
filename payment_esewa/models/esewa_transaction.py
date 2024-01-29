from odoo.exceptions import ValidationError
from odoo import api, fields, models
from datetime import datetime
from odoo.http import request
import logging


_logger = logging.getLogger(__name__)


class EsewaTransaction(models.Model):
    _inherit = 'payment.transaction'   
    ref_id = fields.Char("Esewa Ref")

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

        if self.provider_id.code != 'esewa':
            return res
        
        reference = self.reference
        order_obj = self.env['sale.order'].sudo().search([['name','=',reference.split('-')[0]]])
        amount = int(order_obj['amount_untaxed'])
        total_amount = int(order_obj['amount_total'])
        tax_amount = int(order_obj['amount_tax'])

        value = {
            'amount':str(amount),
            'tax_amount':str(tax_amount),
            'total_amount':str(total_amount),
            'transaction_uuid':reference,
            'success_url':f'{self.provider_id.domain_name}/esewa/successful',
            'failure_url':f'{self.provider_id.domain_name}/esewa/failure',
            'merchant_code':self.provider_id.merchant_code,
            'product_service_charge':"0",
            'product_delivery_charge':"0",
        }
        return value

    def action_esewa_set_done(self):
        """ Set the state of the esewa transaction to 'done'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return

        self._set_done()

    def action_esewa_set_pending(self):
        """ Set the state of the esewa transaction to 'pending'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return

        self._set_pending()

    def action_esewa_set_auth(self):
        """ Set the state of the esewa transaction to 'authorized'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return
        self.action_esewa_set_draft()
        self._set_authorized()


    def action_esewa_set_canceled(self):
        """ Set the state of the esewa transaction to 'cancel'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return

        self._set_canceled()

    def action_esewa_set_error(self):
        """ Set the state of the esewa transaction to 'error'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return

        self._set_error("Error Has Occured Registering This Payment")

    def action_esewa_set_draft(self):
        """ Set the state of the esewa transaction to 'error'.

        Note: self.ensure_one()

        :return: None
        """
        self.ensure_one()
        if self.provider_code != 'esewa':
            return

        self.state = 'draft'






        
        
        
        
    
