import json
from odoo import http
from odoo.http import request
import xmlrpc.client
import jwt
import re



class EcomClientController(http.Controller):
    _valid_sort_keys = ['price','name','date']
    _valid_sort_order = ['asc','desc']
    _flag = 'GGEZ8848'
    _secret = 'H@L0K100GGEZ666'

    def extract_product_data(self,pro,tmp):
        data = {}
        data["id"] = pro.id
        data["name"] = tmp.name
        data["description"] = tmp.description_sale if tmp.description_sale else ""
        data["detailed_type"] = tmp.detailed_type
        data['base_price'] = tmp.list_price
        data['date'] = str(tmp.write_date)
        data['img_url'] = f'{self.get_base_url()}/web/image/product.product/{pro.id}/image_1024/'
        data["default_code"] = pro.default_code if pro.default_code else (tmp.default_code if tmp.default_code else "")
        data["weight"] = pro.weight
        data["volume"] = pro.volume
        data["has_variant"] = False
        data['shipping_time'] = '2 to 3 business days'
        data['guarantee'] = '30 days money back guarantee'

        return data

    def handle_variants_data(self,products_with_variants_ids):
        data_arr = []
        products_combination_str_indices_map = {pro.combination_indices:pro for pro in list(products_with_variants_ids.values())}
        products_combination_obj_indices_map = {}

        for [inds, product] in products_combination_str_indices_map.items():
            product_template_attr_val = [http.request.env['product.template.attribute.value'].sudo().search([('id','=',int(id))]) for id in inds.split(',')]
            products_combination_obj_indices_map[frozenset(product_template_attr_val)] = product
        
        # data rendering starts here
        # for product with variants:
        duplicate_tracker = []
        for [variants, product] in products_combination_obj_indices_map.items():
            tmp = product.product_tmpl_id
            if tmp.id not in duplicate_tracker:
                data = {}
                duplicate_tracker.append(product.product_tmpl_id.id)
                data['tmp_id'] = product.product_tmpl_id.id
                data["name"] = product.product_tmpl_id.name
                data["description"] = product.product_tmpl_id.description_sale if product.product_tmpl_id.description_sale else ""
                data["detailed_type"] = product.product_tmpl_id.detailed_type
                data["base_price"] = product.product_tmpl_id.list_price
                data["default_code"] = product.default_code if product.default_code else (tmp.default_code if tmp.default_code else "")
                data["has_variant"] = True
                data["weight"] = product.weight
                data["volume"] = product.volume
                data["date"] = str(product.product_tmpl_id.write_date)
                data['shipping_time'] = '2 to 3 business days'
                data['guarantee'] = '30 days money back guarantee'
                data_arr.append(data)

            for data_item in data_arr:
                if data_item['tmp_id'] == product.product_tmpl_id.id:
                    data=data_item
        
            if not data.get('variants'):
                data['variants'] = []
            
            var = {}
            variant_props = {}
            for variant in variants:
                variant_props[variant.attribute_id.name] = variant.product_attribute_value_id.name

                if not var.get('price'):
                    var['price'] = product.product_tmpl_id.list_price
                
                var['price'] += variant.price_extra
            
            var['props'] = variant_props
            var['id'] = product.id
            var['img_url'] = f'{self.get_base_url()}/web/image/product.product/{product.id}/image_1024/'
            data['variants'].append(var)

        return data_arr
    
    def paginate(self,list_of_items, page_size, page_number):
        """Paginates a list of items.

        Args:
            list_of_items: A list of items to paginate.
            page_size: The number of items per page.
            page_number: The page number to return.

        Returns:
            A list of items on the specified page.
        """

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return list_of_items[start_index:end_index]

    def get_user(self,user_id):
        return http.request.env["res.users"].sudo().search([('id','=',user_id)])
    
    def get_product(self,tmpl_id):
        return http.request.env["product.product"].sudo().search([('product_tmpl_id','=',int(tmpl_id))])
    
    def get_product_product(self,id):
        return http.request.env["product.product"].sudo().search([('id','=',int(id))])

    def authenticate(self):
        return request.httprequest.headers.get('flag') == 'GGEZ8848'

    def validate_user(self,data={}):
        user_data = data.get('user') if data.get('user') else request.httprequest.headers.get('user')
        if not user_data:
            return False
        try:
            payload = jwt.decode(user_data.encode(),self._secret,algorithms=['HS256'])
            return payload['uid']
        except Exception as err:
            return False

    def get_order_key(self,key):
        if key=='price':
            return 'base_price'
        return key
    
    def convert_model_to_json(self,model):
        data_arr = []

        for rec in model:
            data = {}
            for field in rec._fields:
                data_type=type(rec[field])
                if data_type in [bool,str,int,float]:
                    data[field] = rec[field]
                else:
                    try:
                        data[field] = rec[field].id
                    except Exception:
                        continue

            data_arr.append(data)
        
        if len(data_arr) == 1:
            [data_arr] = data_arr

        return data_arr

    def get_base_url(self):
        return http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')


    @http.route(
        '/api/v1/currencies', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_currencies(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        currencies = http.request.env['res.currency'].search([('active','=',True)])
        return json.dumps({'success':True,'data':currencies.read(['id','name','full_name','symbol'])})
    


    @http.route(
        '/api/v1/delivery/providers', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_carriers(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        carriers = http.request.env['delivery.carrier'].sudo().search([])
        return json.dumps({'success':True,'data':carriers.read(['id','name'])})
    

    def fetch_single_product(self,id,only_obj=False):
        pro = http.request.env['product.product'].sudo().search([('id','=',id)])

        if only_obj:
            return pro


        tmp = pro.product_tmpl_id
        [data] = pro.read(fields=['id'])
        data["name"] = tmp.name
        data["description"] = tmp.description_sale if tmp.description_sale else ""
        data["detailed_type"] = tmp.detailed_type
        data['price'] = tmp.list_price
        # [data['category']] = tmp.categ_id.read(fields=['name'])
        data['img_url'] = f'{self.get_base_url()}/web/image/product.product/{pro.id}/image_1024/'
        combination_indices = pro.combination_indices
        
        if combination_indices:
            attr_val_ids = combination_indices.split(',')

            for id in attr_val_ids:
                value_record = http.request.env['product.template.attribute.value'].sudo().search([('id','=',int(id))])
                data['price']+=value_record.price_extra  

        return data
    

    
    @http.route(
        '/api/v1/terms', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_terms(self):
        request_url = http.request.httprequest.url
        return json.dumps({'success':True,'data':{'url':request_url.replace('/api/v1/terms','/terms')}})
    
    @http.route('/api/v1/countries',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_countries(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        countries = http.request.env['res.country'].sudo().search([])
        return json.dumps({
            'success':True,
            'data':countries.read(['id','name','code'])
        })
        
    @http.route('/api/v1/countries/<country_id>',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_country(self,country_id):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        countries = http.request.env['res.country'].sudo().search([('id','=',int(country_id))])
        return json.dumps({
            'success':True,
            'data':countries.read(['id','name','code'])
        })
    
    @http.route('/api/v1/companies',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_companies(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        countries = http.request.env['res.company'].sudo().search([])
        return json.dumps({
            'success':True,
            'data':countries.read(['id','name'])
        })
    
    @http.route('/api/v1/companies/<company_id>',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_company(self,company_id):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        countries = http.request.env['res.company'].sudo().search([('id','=',int(company_id))])
        return json.dumps({
            'success':True,
            'data':countries.read(['id','name'])
        })

    @http.route('/api/v1/websites',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_websites(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        countries = http.request.env['website'].sudo().search([])
        return json.dumps({
            'success':True,
            'data':countries.read(['id','name'])
        })


