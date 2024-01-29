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

        # product_template_without_variants_ids = {pro.product_tmpl_id.id:pro.product_tmpl_id for pro in products if not pro.combination_indices}
        # product_template_with_variants_ids = {pro.product_tmpl_id.id:pro.product_tmpl_id for pro in products if pro.combination_indices}

        products_combination_str_indices_map = {pro.combination_indices:pro for pro in list(products_with_variants_ids.values())}
        products_combination_obj_indices_map = {}

        for [inds, product] in products_combination_str_indices_map.items():
            product_template_attr_val = [http.request.env['product.template.attribute.value'].sudo().search([('id','=',int(id))]) for id in inds.split(',')]
            products_combination_obj_indices_map[frozenset(product_template_attr_val)] = product
        
        # data rendering starts here
        # for product with variants:
        data_arr = []
        duplicate_tracker = []
        for [variants, product] in products_combination_obj_indices_map.items():
            
            if product.product_tmpl_id.id not in duplicate_tracker:
                data = {}
                duplicate_tracker.append(product.product_tmpl_id.id)
                data["tmp_id"] = product.product_tmpl_id.id
                data["name"] = product.product_tmpl_id.name
                data["description"] = product.product_tmpl_id.description_sale if product.product_tmpl_id.description_sale else ""
                data["detailed_type"] = product.product_tmpl_id.detailed_type
                data["base_price"] = product.product_tmpl_id.list_price
                data["default_code"] = product.default_code if product.default_code else product.product_tmpl_id.default_code
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

                
        product_variant_wishlist = []
        #for product without variants:
        for [id,pro] in products_without_variants_ids.items():
            data = {}
            tmp = pro.product_tmpl_id
            data["id"] = pro.id
            data["name"] = tmp.name
            data["description"] = tmp.description_sale if tmp.description_sale else ""
            data["detailed_type"] = tmp.detailed_type
            data['base_price'] = tmp.list_price
            data['date'] = str(tmp.write_date)
            data['img_url'] = f'{self.get_base_url()}/web/image/product.product/{pro.id}/image_1024/'
            data["default_code"] = pro.default_code if pro.default_code else tmp.default_code
            data["weight"] = pro.weight
            data["volume"] = pro.volume
            data['shipping_time'] = '2 to 3 business days'
            data['guarantee'] = '30 days money back guarantee'
            data_arr.append(data)


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
    
     