from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import tools
from odoo.tools import ustr, pycompat, formataddr, email_normalize, encapsulate_email, email_domain_extract, email_domain_normalize
import logging

_logger = logging.getLogger(__name__)

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.model
    def next_by_code(self, sequence_code, sequence_date=None):
        self.check_access_rights('read')
        company_id = self.env.company
        if company_id.is_local_entity:
            company_id = company_id.id
        elif company_id.parent_id.is_local_entity:
            company_id = company_id.parent_id.id
        else:
            company_id = company_id.id
        seq_ids = self.search([('code', '=', sequence_code), ('company_id', 'in', [company_id, False])], order='company_id')
        print(seq_ids)
        if not seq_ids:
            _logger.debug("No ir.sequence has been found for code '%s'. Please make sure a sequence is set for current company." % sequence_code)
            return False
        seq_id = seq_ids[0]
        return seq_id._next(sequence_date=sequence_date)