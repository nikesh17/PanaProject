from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

from odoo.http import request


class CustomWebsiteSale(WebsiteSale):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def shop_payment(self, **post):
        # response = super(CustomWebsiteSale, self).shop_payment(**post)  # Get the original content of /shop/payment
        print("from controller")
        print(request)
        print(type(request.httprequest.environ['PATH_INFO']))
        route = request.httprequest.environ['PATH_INFO'] if request else None
        print(route)
        # Get the order
        order = request.website.sale_get_order()
        negotiation_token = post.get('negotiation_token')
        promo_code = post.get('promo_code')
        print(type(promo_code))
        print(promo_code)
        request.promo_code = promo_code
        # return super(CustomWebsiteSale, self).shop_payment(**post)


        # modified_template = request.render('price_negotiation.inserting_default_value_negotiation_code',{
        #     'promo_code': promo_code
        # })
        # original_content = response.qcontext.get('website_sale_payment')  # Retrieve the original content or empty string
        # print(original_content)
        # response.qcontext['website_sale_payment'] = original_content + modified_template
        # return response
        if negotiation_token:
            # Query the database to check if the negotiation token exists
            existing_token = http.request.env['price.negotiation'].sudo().search([('negotiation_token','=',negotiation_token)])
        
            if existing_token:
                print(negotiation_token)
                return super(CustomWebsiteSale, self).shop_payment(**post)
            else:
                return http.request.redirect('/shop')
        else:
            return super(CustomWebsiteSale, self).shop_payment(**post)


    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        request.promo_code = None
        return super().cart(access_token=None, revive='', **post)

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(
        self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
        product_custom_attribute_values=None, no_variant_attribute_values=None, **kw
    ):
        request.promo_code = None
        print()
        return super().cart_update_json(product_id, line_id, add_qty, set_qty, display, product_custom_attribute_values, no_variant_attribute_values, **kw)