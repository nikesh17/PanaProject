from odoo import http
from odoo.http import request
import json
from odoo.addons.portal.controllers import portal


class Main(http.Controller):

    @http.route("/home", auth='user', website=True)
    def show_product(self, **kwargs):
        products = request.env['product.template'].search([])

        return request.render('product_portal.show_product', {'products': products})


# Portal Extend Class
class CustomerPortal(portal.CustomerPortal):

    # Query Product Count by method overriding from portal module
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'product_count' in counters:
            count = request.env['price.negotiation'].search_count([])
            values['product_count'] = count
        return values

    @http.route('/my/negotiations', auth="user", website=True)
    def portal_my_product(self, **kwargs):
        products = request.env['price.negotiation'].search([])
        print("portal")


        return request.render("product_portal.portal_products", {'products': products,})

    @http.route('/my/products/<model("price.negotiation"):product>/', auth='user', website=True)
    def display_course_detail(self, product):
        return http.request.render('product_portal.product_detail', {'product': product, 'page_name': 'product'})

    @http.route('/update_negotiation_record',methods=['POST'], auth="user", website=True,csrf=False)
    def get_edit_option(self, **kwargs):
        negotiation_request_payload = request.httprequest.data.decode('utf-8')  # Decode bytes to string
        negotiation_id = json.loads(negotiation_request_payload).get('negotiation_id')
        new_expected_price = json.loads(negotiation_request_payload).get('updated_expected_price')
        new_customer_status = json.loads(negotiation_request_payload).get('updated_customer_status')
        # new_updated_quantity = json.loads(negotiation_request_payload).get('updated_quantity')
        print(new_expected_price)
        print(new_customer_status)
        # print(new_updated_quantity)
        print(negotiation_id)
        if negotiation_id:

            negotiation_record = request.env['price.negotiation'].browse(int(negotiation_id))
            negotiation_record.write({
                'expected_price_per_unit': new_expected_price,
                'customer_status': new_customer_status,
                # 'quantity': new_updated_quantity
            })
            # print(negotiation_record.customer)
            # print(negotiation_record)
            negotiation_data = {
                'negotiation_id': negotiation_id
            }

            return request.make_response(json.dumps(negotiation_data),headers=[('Content-Type','application/json')])
        else:
            print("We are not able te fetch data from the server")

    @http.route('/delete/negotiation-request/<int:negotiation_id>',methods=['DELETE'],auth="user",website=True,csrf=False)
    def delete_negotiation_request_record(self, **kwargs):
        negotiation_id = kwargs.get('negotiation_id')
        try:
            # Assuming 'your.negotiation.model' is the model containing negotiation records
            negotiation_record = request.env['price.negotiation'].browse(int(negotiation_id))

            if negotiation_record:
                negotiation_record.unlink()  # Delete the record
                return "Record deleted successfully!"
            else:
                return "Record not found or already deleted!"

        except Exception as e:
            return f"Error: {e}"