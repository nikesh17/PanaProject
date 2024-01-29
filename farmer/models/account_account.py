from odoo import api, fields, models, _
from odoo.tools import remove_accents
import random

def is_encodable_as_ascii(string):
    try:
        remove_accents(string).encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

class FarmerAccAcc(models.Model):
    _inherit='account.account'
    copy_mode = fields.Boolean(default=False)

    @api.constrains('account_type')
    def _check_account_type_unique_current_year_earning(self):
        if self.copy_mode:
            return 
        
        super(FarmerAccAcc,self)._check_account_type_unique_current_year_earning()

class FarmerAccJournal(models.Model):
    _inherit='account.journal'
    copy_mode = fields.Boolean(default=False)

    def _inverse_type(self):
        # Create an alias for purchase/sales journals
        for journal in self:
            if journal.type not in ('purchase', 'sale'):
                if journal.alias_id:
                    journal.alias_id.sudo().unlink()
                continue

            alias_name = next(string for string in (
                journal.alias_name,
                journal.name,
                journal.code,
                journal.type,
            ) if string and is_encodable_as_ascii(string))
            
            if self.copy_mode:
                random_bits = random.getrandbits(128)
                hash = "%032x" % random_bits
                alias_name = f'{alias_name} [{hash}]'

            if journal.company_id != self.env.ref('base.main_company'):
                if is_encodable_as_ascii(journal.company_id.name):
                    alias_name = f"{alias_name}-{journal.company_id.name}"
                else:
                    alias_name = f"{alias_name}-{journal.company_id.id}"

            alias_values = {
                'alias_defaults': {
                    'move_type': 'in_invoice' if journal.type == 'purchase' else 'out_invoice',
                    'company_id': journal.company_id.id,
                    'journal_id': journal.id,
                },
                'alias_parent_thread_id': journal.id,
                'alias_name': alias_name,
            }
            if journal.alias_id:
                journal.alias_id.sudo().write(alias_values)
            else:
                alias_values['alias_model_id'] = self.env['ir.model']._get('account.move').id
                alias_values['alias_parent_model_id'] = self.env['ir.model']._get('account.journal').id
                journal.alias_id = self.env['mail.alias'].sudo().create(alias_values)
        self.invalidate_recordset(['alias_name'])