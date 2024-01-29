# from odoo.addons.web.controllers.home import Home
from odoo.http import request
from odoo import http,api,SUPERUSER_ID
from odoo.addons.web.controllers.home import Home

class LoginPageInherit(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        try:
            hosturl = request.httprequest.environ['HTTP_REFERER'] if request else 'n/a'
            hosturl = hosturl[hosturl.index('://')+3:]
            hosturl = hosturl[:hosturl.index('/')]
            company_detail = http.request.env["res.company.details"].sudo().search([('url','=',hosturl)])
            company = company_detail.parent_id

            request.company_bg_img = company.login_bg_img
            request.company_palika_info = company.palika.palika_name
            request.company_title1 = "Office of " + str(company.palika.type) + ' executive'
            request.company_title2 = company.street 
            request.company_title3 = str(company.province.name) + ', Nepal'
            res = super().web_login(redirect,**kw)
        except:
            res = super().web_login(redirect,**kw)
        return res