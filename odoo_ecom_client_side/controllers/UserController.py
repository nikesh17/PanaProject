import json
from odoo import http
from odoo.http import request
import xmlrpc.client
import jwt
from . import main
import odoo.addons.base.models.res_users as ResUser


class UserController(main.EcomClientController):
    @http.route(
        '/api/v1/register', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def register(self, **data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        json_data = json.loads(request.httprequest.data)
        name = data.get('name') if data.get('name') else json_data.get("name") 
        login = data.get('login') if data.get('login') else json_data.get("login")
        password = data.get('password') if data.get('password') else json_data.get("password")
        company_id = data.get('company_id') if data.get('company_id') else json_data.get("company_id")

        if not name or not password:
            return json.dumps({"success": False, "message": "Sorry, username and password must be present"})

        if not login:
            return json.dumps({"success": False, "message": "Sorry, username and password must be present"})
        
        data = {
            'name': name,
            'login': login,
            'password': password,        
            'company_id':int(company_id)
        }

        http_env = http.request.env
        http_env.context = {'allowed_company_ids':[data.get('company_id')]}
        user = http_env.user.create(data)
        user.share = True


        user.groups_id = [(3,http_env.ref('base.group_public').id)]
        user.groups_id = [(3,http_env.ref('base.group_user').id)]
        user.groups_id = [(4,http_env.ref('base.group_portal').id)]
        

        return json.dumps({'success': True, 'data': user.read(fields=['id','login'])})


    @http.route(
        '/api/v1/linkUser', type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def getuser(self,**data):
        # _payment=http.request.env['payment.provider'].sudo().search([('code','=','demo')])
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        
        if not request.httprequest.data:
            return json.dumps({"success":False,"message":"Sorry, username and password must be present"})

        json_data =json.loads(request.httprequest.data)
        login = data.get('login') if data.get('login') else json_data.get("login") 
        password = data.get('password') if data.get('password') else json_data.get("password")

        if not login or not password:
            return json.dumps({"success":False,"message":"Sorry, login info and password must be present"})
        
        uid = http.request.env['res.users'].api_login(request.db,login, password,{})

        if not uid:
            return json.dumps({"success":False,"message":"Sorry, wrong login info or password"})

        payload = {
            "uid": uid,
        }
        token = jwt.encode(payload, self._secret, algorithm='HS256')
        return json.dumps({"success":True,"data":token})

    @http.route('/api/v1/user/add_address',type='http',auth='public',methods=['POST'],csrf=False,save_session=False)
    def add_address(self,**data):
        try:
            json_data = json.loads(request.httprequest.data)
            required_fields = ['name','email','phone','zip','city','street']
            all_fields = ['company_name','vat','steet2',*required_fields]
            create_data = {}


            for field in required_fields:
                field_data = json_data.get(field)
                
                if not field_data:
                    return json.dumps({
                        'success':False,
                        'message':f'The following required field is missing: {field}'
                    })

                create_data[field] = field_data


        except Exception as e:
            return json.dumps({
                'success':False,
                'message':'Wrong data format provided.'
            })


        partner_model = http.request.env['res.partner']
        country = http.request.env['res.country'].sudo().search([('name','=','Nepal')])
        create_data['country_id'] = country.id
        partner = partner_model.sudo().create(create_data)
        
        return json.dumps({
            'success':True,
            'data':{'parter_id':partner.id},
            'message':'Contact(Partner) created successfully'
            
        })


    @http.route('/api/v1/user/update_user',type='http',auth='public',methods=['POST'],csrf=False,save_session=False)
    def update_user(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        user_id = self.validate_user()   

        if not user_id:
            return json.dumps({'success':False,'message':'User data not provided'})  

        try:
            json_data = json.loads(request.httprequest.data)
    

        except Exception as e:
            return json.dumps({
                'success':False,
                'message':'Wrong data format provided. JSON data must be provided'
            })


        user = self.get_user(user_id)
        login = json_data.get('login')
        password = json_data.get('password')

        if login:
            user.login = login
            json_data.pop('login')

        if password:
            user.write({
                'password':password
            })
            json_data.pop('password')

            
        partner = user.partner_id
        partner.sudo().write(json_data)
            
        
        return json.dumps({
            'success':True,
            'message':"User data updated successfully."
        })
    

    @http.route('/api/v1/user/change_password',type='http',auth='public',methods=['POST'],csrf=False,save_session=False)
    def change_password(self,**data):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        user_id = self.validate_user()     
        if not user_id:
            return json.dumps({'success':False,'message':'User data not provided'})
        
        try:
            json_data = json.loads(request.httprequest.data)
    

        except Exception as e:
            return json.dumps({
                'success':False,
                'message':'Wrong data format provided. JSON data must be provided'
            })
        
        password = json_data.get('password')
        confirm_password = json_data.get('confirm_password')

        if not password:
            return json.dumps({'success':False,'message':'Password is required'})
        
        if not confirm_password:
            return json.dumps({'success':False, 'message':'Confirm Password data is required'})
        
        if password!=confirm_password:
            return json.dumps({'success':False,'message':'Password and confirm password field must match'})
        
        user = self.get_user(user_id)


        user.write({    
            'password':password
        })

      
        
        return json.dumps({
            'success':True,
            'message':"Password changed successfully."
        })
    


    

    @http.route('/api/v1/user/contact_status',type='http',auth='public',methods=['GET'],csrf=False,save_session=False)
    def get_address_status(self):
        if not self.authenticate():
            return json.dumps({'success':False,'message':'You dont have the required api permission'})
        uid = self.validate_user()
        if not uid:
            return json.dumps({'success':False,'message':'You need to provide the valid user data'})
        
        partner = self.get_user(uid).partner_id
        [address_dict] = partner.read([
            'street',
            'street2',
            'country_id',
            'zip',
            'city',
            'phone',
            'mobile',
            'email',
            'name'
        ])

        address_dict['country'] = address_dict['country_id'][1]
        del address_dict['country_id']

        for key,value in address_dict.items():
            if not value:
                address_dict[key] = None

        return json.dumps({
            'success':True,
            'data':address_dict,

        })
    



            

            

            
            
        

        
