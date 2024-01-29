from odoo import http
from odoo.http import request, Controller, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(Controller):
    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.

        Does not include the record counts.
        """
        # get customer sales rep
        sales_user_sudo = request.env["res.users"]
        partner_sudo = request.env.user.partner_id
        if partner_sudo.user_id and not partner_sudo.user_id._is_public():
            sales_user_sudo = partner_sudo.user_id

        return {
            "sales_user": sales_user_sudo,
            "page_name": "home",
        }

    @route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("upabhokta_samiti.cust_portal_account", values)


class WebsiteMenuController(http.Controller):
    @http.route("/register", type="http", auth="public", website=True)
    def website_menu_controller(self):
        return request.render("upabhokta_samiti.portal_register_categories_page", {})
