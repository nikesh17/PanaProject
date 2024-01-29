from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import tools
from odoo.tools import ustr, pycompat, formataddr, email_normalize, encapsulate_email, email_domain_extract, email_domain_normalize

class MailServer(models.Model):
    _inherit = 'ir.mail_server'
    _description= 'Mail server '

    def _get_default_company(self):
        if "allowed_company_ids" in dict(self.env.context).keys():
            res = self.env.context["allowed_company_ids"][0]
        else:
            res = 1
        res = self.env["res.company"].search([('id','=',res)])[0]
        return res

    company_id = fields.Many2one("res.company","Associated Company",default=_get_default_company)


    def _find_mail_server(self, email_from, mail_servers=None):
        """Find the appropriate mail server for the given email address.

        Returns: Record<ir.mail_server>, email_from
        - Mail server to use to send the email (None if we use the odoo-bin arguments)
        - Email FROM to use to send the email (in some case, it might be impossible
          to use the given email address directly if no mail server is configured for)
        """
        email_from_normalized = email_normalize(email_from)
        email_from_domain = email_domain_extract(email_from_normalized)
        notifications_email = email_normalize(self._get_default_from_address())
        notifications_domain = email_domain_extract(notifications_email)
        if mail_servers is None:
            mail_servers = self.sudo().search([], order='sequence')
        # 0. Archived mail server should never be used
        mail_servers = mail_servers.filtered('active')
        # 1. Try to find a mail server for the right mail from
        # print('--------------mail server------------------')
        # print(self.env['res.company'].search([('id','in',self._context["allowed_company_ids"])]))
        # print(self.env['res.company'].search([('id','in',self._context["allowed_company_ids"])]).name)
        try:
            print(self._context["allowed_company_ids"])
            allowed_companies = self.env['res.company'].search([('id','in',self._context["allowed_company_ids"])])
            temp = []
            for comp in allowed_companies:
                if comp.is_local_entity:
                    temp.append(comp.id)
                elif comp.parent_id.is_local_entity:
                    temp.append(comp.parent_id.id)
            mail_servers = mail_servers.filtered(lambda m: m.company_id.id in temp)
        except:
            pass
        print(mail_servers)
        print(mail_servers.name)
        mail_server = mail_servers.filtered(lambda m: email_normalize(m.from_filter) == email_from_normalized)
        if mail_server:
            return mail_server[0], email_from

        mail_server = mail_servers.filtered(lambda m: email_domain_normalize(m.from_filter) == email_from_domain)
        if mail_server:
            return mail_server[0], email_from

        # 2. Try to find a mail server for <notifications@domain.com>
        if notifications_email:
            mail_server = mail_servers.filtered(lambda m: email_normalize(m.from_filter) == notifications_email)
            if mail_server:
                return mail_server[0], notifications_email

            mail_server = mail_servers.filtered(lambda m: email_domain_normalize(m.from_filter) == notifications_domain)
            if mail_server:
                return mail_server[0], notifications_email

        # 3. Take the first mail server without "from_filter" because
        # nothing else has been found... Will spoof the FROM because
        # we have no other choices
        mail_server = mail_servers.filtered(lambda m: not m.from_filter)
        if mail_server:
            return mail_server[0], email_from

        # 4. Return the first mail server even if it was configured for another domain
        if mail_servers:
            return mail_servers[0], email_from

        # 5: SMTP config in odoo-bin arguments
        from_filter = self.env['ir.config_parameter'].sudo().get_param(
            'mail.default.from_filter', tools.config.get('from_filter'))

        if self._match_from_filter(email_from, from_filter):
            return None, email_from

        if notifications_email and self._match_from_filter(notifications_email, from_filter):
            return None, notifications_email

        return None, email_from