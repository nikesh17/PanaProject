import json
from odoo import http
from . import main
import base64
import random
import statistics



class ReviewController(main.EcomClientController):

    def get_mimetype(self,extention):
        if extention in ['jpg','jpeg','png']:
            return f'image/{extention}'
        elif extention == 'pdf':
            return 'application/pdf'
        return False



    @http.route(
        '/api/v1/reviews/<product_id>', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_reviews(self,product_id):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        product = http.request.env['product.product'].sudo().search([('id','=',int(product_id))])

        if not product:
            return json.dumps({'success':False,'message':'Sorry, the product you requested doesn\'t exist'})
        reviews = http.request.env['rating.rating'].sudo().search([('res_model','=','product.template')])
        product_template = product.product_tmpl_id

        rating_stats = {}
        data_arr =[]
        filtered_reviews = [review for review in reviews if int(review.message_id.res_id) == int(product_template.id)]
        rating_arr = [review['rating'] for review in filtered_reviews]
        count = len(rating_arr)
        average = 0
        if rating_arr:
            average = statistics.mean(rating_arr)


        for review in filtered_reviews:
            [review_dict] = review.read(['id','res_name','feedback','rating','files','write_date','partner_id'])
            review_dict['posted_date'] = str(review_dict['write_date'])
            review_dict['user'] = review_dict['partner_id'][1]
            user = http.request.env['res.users'].sudo().search([('partner_id','=',int(review_dict['partner_id'][0]))])
            review_dict['profile_pic'] = f'{self.get_base_url()}/web/image?model=res.users&id={user.id}&field=avatar_1024'
            del review_dict['partner_id']
            del review_dict['write_date']
            data_arr.append(review_dict)

        for [review,review_obj] in zip(data_arr,filtered_reviews):
            file_urls = []
            for file in review_obj.files:
                file_urls.append(f'{self.get_base_url()}/web/content/{file.id}?access_token={file.access_token}')
            review['files'] = file_urls
            review['product_name'] = review['res_name']
            del review['res_name']

        return json.dumps({
            'success':True,
            'data': data_arr,
            'rating_stats': {
                'total':count,
                'average':average
            }
        })
    

    @http.route(
        '/api/v1/reviews/', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def post_review(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        user_id = self.validate_user()
        if not user_id:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})

        try:
            product_id = data.get("product_id")
            feedback = data.get('feedback')

            try:
                rating = float(int(data.get('rating')))
            except Exception as e:
                return json.dumps({'success':False,'message':'Rating must not be empty and must be numeric values'})
            
            if not product_id:
                return json.dumps({'success':False,'message':'Product ID must be provided'})
            
            if not feedback:
                return json.dumps({'success':False,'message':'Feedback must be provided'})
            
            parent_id = data.get('parent_id')

            if rating > 5:
                return json.dumps({'success':False,'message':'The rating must be between 0 and 5'})
        except Exception as e:
            print(e)
            return json.dumps({'success':False,'message':f'Wrong data format provided, You provided the following values: product_id:{product_id}, feedback:{feedback} and rating:{rating}.'})
        

        attachment_ids = []
        attachment_access_token = []
        attachments = []

        for key, value in data.items():
            if not value or 'file' not in key:
                continue
            file_name = value.filename
            file_type = file_name.split('.')[1]
            mimetype = self.get_mimetype(file_type)

            if not mimetype:
                return json.dumps({'success':False, 'message':'Wrong file format provided, only supports: pdf, png, jpeg and jpg file formats.'})

            attachment = http.request.env['ir.attachment'].sudo().create({
                'name': f'{value.filename}',
                'datas': base64.encodebytes(value.read()),
                'res_model': 'product.template',
                'res_id': int(product_id),
                'mimetype': mimetype,
            })
            random_bits = random.getrandbits(128)
            attachment.access_token = "%032x" % random_bits
            attachment_ids.append(attachment.id)
            attachment_access_token.append(attachment.access_token)
            attachments.append(attachment)
        
        product = http.request.env['product.product'].sudo().search([('id','=',int(product_id))])
        if not product:
            return json.dumps({'success':False,'message':'Sorry, the product you requested doesn\'t exist'})
        product_template = product.product_tmpl_id
        ir_model = http.request.env['ir.model'].sudo().search([('model','=','product.template')])
        user = self.get_user(user_id)


        data_dict = {
            'feedback':feedback,
            'rating':rating,
            'res_id':product_template.id,
            'res_model_id':ir_model.id,
            'partner_id':user.partner_id.id,
            'consumed':True,
        }
        rating = http.request.env['rating.rating'].sudo().create(data_dict)

        mail_message = http.request.env['mail.message'].sudo().create({
            'author_id': user.partner_id.id,
            'res_id':rating.res_id,
            'model':rating.res_model,
            'message_type':'comment',
            'attachment_ids':attachment_ids,
            'parent_id':parent_id if parent_id else None
            
        })
        mail_message.body = f'<p>{feedback}</p>'
        rating.rating_text='top'
        rating.message_id = mail_message.id

        for attachment in attachments:
            rating.files += attachment

        return json.dumps({
            'success':True,
            'data': 'Review Added Successfully'
        })



