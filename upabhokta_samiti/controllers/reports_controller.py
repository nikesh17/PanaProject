from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal


class ReportsController(http.Controller):
    @http.route(
        "/upabhokta-samiti/darta-nibedan/<model('upabhokta.samiti.info'):id>",
        auth="user",
        type="http",
        website=True,
    )
    def Upabhokta_samiti_darta_nibedan(self, id, **kw):
        portal_controller = CustomerPortal()

        return portal_controller._show_report(
            model=id,
            report_type="pdf",
            report_ref="upabhokta_samiti.Darta_Nibedan",
            download=True,
        )

    @http.route(
        "/upabhokta-samiti/pramadpatra-report/<model('upabhokta.samiti.info'):id>",
        auth="user",
        type="http",
        website=True,
    )
    def Upabhokta_samiti_karyabidhi(self, id, **kw):
        portal_controller = CustomerPortal()

        return portal_controller._show_report(
            model=id,
            report_type="pdf",
            report_ref="upabhokta_samiti.karyabidi_dafa_pramadpatra",
            download=True,
        )

    @http.route(
        "/upabhokta/general-report/<model('upabhokta.samiti.info'):id>",
        auth="user",
        type="http",
        website=True,
    )
    def upabhokta_samiti_general(self, id, **kw):
        portal_controller = CustomerPortal()

        return portal_controller._show_report(
            model=id,
            report_type="pdf",
            report_ref="upabhokta_samiti.general_upabhokta_catalog",
            download=True,
        )
