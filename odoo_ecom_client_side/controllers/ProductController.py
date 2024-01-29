import json
from odoo import http
import re
from . import main


class ProductController(main.EcomClientController):

    
    def get_sort_key(self,id):

        _sort_types = {
                1:['name','asc'],
                2:['name','desc'],
                3:['price','asc'],
                4:['price','desc'],
                5:['date','asc'],
                6:['date','desc']
            }

        return_value = _sort_types.get(id)

        if return_value:
            return return_value

        return False


    @http.route(
        '/api/v1/products/sortTypes', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_sort_types(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        return json.dumps({'success':True,'data':[
            {'id':1,'sort_type':'Name(A-Z)'},
            {'id':2,'sort_type':'Name(Z-A)'},
            {'id':3,'sort_type':'Price - Low to high'},
            {'id':4,'sort_type':'Price - High to Low'},
            {'id':5,'sort_type':'Oldest Arrival'},
            {'id':6,'sort_type':'Newest Arrival'},
        ]})   

    # for all products
    @http.route(
        '/api/v1/products', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_products(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        uid = self.validate_user(kw)

        partner = None
        if uid:
            partner = self.get_user(uid).partner_id
        
        category = kw.get('category')
        order = kw.get('sortBy')
        min_price = kw.get('min_price')
        max_price = kw.get('max_price')
        page_number = int(kw.get('page')) if kw.get('page') else 1
        limit = int(kw.get('limit')) if kw.get('limit') else 10
        search = kw.get('search')

        templates = []

       

        if category:
            category_objs = http.request.env['product.public.category'].sudo().search([])
            category_obj_search = http.request.env['product.public.category'].sudo().search([('id','=',category)])

            if not category_obj_search:
                return json.dumps({'success':False,'message':'Sorry, the category does not exist.'})

            for category_obj in category_objs:
                if str(category) in category_obj.parent_path.split('/'):
                    if not templates:
                        templates = category_obj.product_tmpl_ids
                    else:
                        templates+=category_obj.product_tmpl_ids
                  
        else:
            templates = http.request.env['product.template'].sudo().search([])
        

        template_ids = {tmp.id:tmp for tmp in templates}
        products = http.request.env['product.product'].sudo().search([('product_tmpl_id','in',tuple(template_ids.keys()))])

        products_without_variants_ids = {pro.id:pro for pro in products if not pro.combination_indices}
        products_with_variants_ids = {pro.id:pro for pro in products if pro.combination_indices}

        data_arr = []

        data_arr = [*data_arr,*self.handle_variants_data(products_with_variants_ids)]





        product_variant_wishlist = []
        #for product without variants:
        for [id,pro] in products_without_variants_ids.items():
            tmp = pro.product_tmpl_id
            data = self.extract_product_data(pro,tmp)
            data_arr.append(data)

        for data in data_arr:
            if data['has_variant']:
                data['id'] = data['variants'][0]['id']
                data['img_url'] = data['variants'][0]['img_url']
                data['base_price'] = data['variants'][0]['price']

                del data['variants']
                del data['tmp_id']

        if partner:
            for item in data_arr:
                item['in_wishlist'] = False
                wishlist_records = http.request.env['product.wishlist'].sudo().search([('partner_id','=',partner.id)])
                wishlist_products = [item.product_id.id for item in wishlist_records]

                variants = item.get('variants')



                if not variants:
                    if item['id'] in wishlist_products:
                        item['in_wishlist'] = True
                
                else:
                    variants_ids = [var['id'] for var in variants]

                    for id in variants_ids:
                        if id in wishlist_products:
                            product_variant_wishlist.append(item)


                
                
                    

        for item in product_variant_wishlist:
            item['in_wishlist'] = True
        if search:
            search = search.lower()
            data_arr = [data for data in data_arr if search in data['name'].lower() or search in data['description'].lower()]

        if min_price:
            data_arr = [data for data in data_arr if data['base_price'] >= float(min_price)]


        if max_price:
            data_arr = [data for data in data_arr if data['base_price'] <= float(max_price)]




        if order:
            order_arr = self.get_sort_key(int(order))


            if not order_arr:
                return json.dumps({'success':False,'message':'Wrong Sort ID provided'})
            
            order_key = order_arr[0]
            sort_order = order_arr[1]

            if order_key not in self._valid_sort_keys:
                return json.dumps({'success':False,'message':'Wrong sort key provided, sorting can be done on the basis of price, name and date'})

            if sort_order not in self._valid_sort_order:
                return json.dumps({'success':False,'message':'Wrong sort order provided, sorting can be done on the following orders only: asc, desc'})
            
            data_arr = sorted(data_arr,key=lambda item:item[self.get_order_key(order_key)],reverse=True if sort_order=='desc' else False)


        total_items=len(data_arr)
        total_pages = total_items / limit
        total_pages_int = int(total_pages)
        if total_pages > total_pages_int:
            total_pages_int+=1

        

        if page_number and limit:
            data_arr = self.paginate(data_arr,int(limit),int(page_number))

        for data in data_arr:
            data.pop('date')

        response_data = {'success':True, 'data':data_arr,'meta':{'total_records':total_items,'last_page':total_pages_int,'current_page':page_number, 'per_page':limit,}}
        
        if page_number and limit:
            print(page_number, limit)
            page_number = int(page_number)
            limit = int(limit)
            request_url = http.request.httprequest.url
            previous_pn = int(page_number)-1
            next_pn = int(page_number)+1
            

            if page_number>1:
                if 'page' in request_url:
                    response_data['meta']['previous_url'] = str(re.sub(r"page=\d",f'page={previous_pn}',request_url))
                elif '?' in request_url:
                    response_data['meta']['previous_url'] = f'{request_url}&page={previous_pn}'
                else:
                    response_data['meta']['previous_url'] = f'{request_url}?page={previous_pn}'
            if page_number * limit < total_items:    
                if 'page' in request_url:  
                    response_data['meta']['next_url'] = str(re.sub(r"page=\d",f'page={next_pn}',request_url))

                elif '?' in request_url:
                    response_data['meta']['next_url'] = f'{request_url}&page={next_pn}'

                else:
                    response_data['meta']['next_url'] = f'{request_url}?page={next_pn}'

        return json.dumps(response_data)
    
     


    # for single product
    @http.route(
        '/api/v1/products/<int:id>', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
   )
    def get_product(self,**kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        id = kw.get('id')
        product_reference = self.fetch_single_product(id,True)
        print(product_reference)
        template = product_reference.product_tmpl_id
        products = http.request.env['product.product'].search([('product_tmpl_id','=',template.id)])
        products_with_variants_ids = {pro.id:pro for pro in products}
        if len(products)==1:
            return json.dumps({'success':True,'data':self.extract_product_data(products,template)})
        [data] = self.handle_variants_data(products_with_variants_ids)
        del data['tmp_id']
        del data['has_variant']

        

        return json.dumps({'success':True,'data':data})


    # for product category
    @http.route(
        '/api/v1/products/category', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_product_categories(self, **kw):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        records = http.request.env['product.public.category'].sudo().search([])
        records_dict = records.read(fields=['id','name','parent_id'])
        children_tracker = []

        for item in records_dict:
            item['children'] = []
            if item.get('parent_id'):
                item['parent_id'] = item['parent_id'][0]


            for rec in records:
                id_str = str(item['id'])
                parent_path_ids = rec.parent_path.split('/')
                if id_str in parent_path_ids and item['id']!=rec.id:
                    item['children'].append({'id':rec.id,'name':rec.name})
                    children_tracker.append(int(rec.id))

        final_data=[]

        for item in records_dict:
            if int(item.get('id')) in children_tracker:
                continue

            if not item['children']:
                item['children']=None
            final_data.append(item)
                

        # print(children_tracker)
        return json.dumps({'success':True,'data':final_data})
    

    @http.route(
        '/api/v1/products/pricelists', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_pricelists(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})

        price_list = http.request.env['product.pricelist'].sudo().search([])
        return json.dumps({'success':True,'data':price_list.read(['id','name'])})
