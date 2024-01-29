from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from datetime import datetime
import requests
import pprint
import logging

_logger = logging.getLogger(__name__)


class KhaltiProvider(models.Model):
    _inherit = 'payment.provider'
    _api_endpoint = '/epayment/initiate/'
    _lookup_endpoint = '/epayment/lookup/'

    domain_name = fields.Char(_("Server Domain"),default="http://localhost")
    port=fields.Char(_("Port Number"),default="8069")
    
    code = fields.Selection(
        selection_add=[('khalti', "khalti")], ondelete={'khalti': 'set default'}
    )
    khalti_auth_key=fields.Char(string=_('Khalti Authorization Key'), required_id_provider="khalti", groups='base.group_system')
    khalti_url = fields.Char(string=_('Khalti Url'))

    
    def _khalti_get_api_url(self):
        """ Return the API URL according to the provider state.

        Note: self.ensure_one()

        :return: The API URL
        :rtype: str
        """
        self.ensure_one()
        return self.khalti_url
        
    def _make_khalti_request(self,payload,mode="initiate"):
  
        self.ensure_one()
        
        if mode=="initiate":      
            url=f"{self._khalti_get_api_url()}{self._api_endpoint}"
        elif mode=="lookup":
            url=f"{self._khalti_get_api_url()}{self._lookup_endpoint}"
        
        headers = {
            "Authorization": f"key {self.khalti_auth_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
                )
                raise ValidationError("Khalti: " + _(
                    "The communication with the API failed. Khalti gave us the following "
                    "information: '%s'", response.json().get('message', '')
                ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Khalti: " + _("Could not establish the connection to the API.")
            )
        return response.json()
                
