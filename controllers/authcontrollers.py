from openerp import http,models
from openerp.http import request
from openerp.tools.translate import _
from jsonhelper import JsonHelper
import operator
import datetime
import json
import logging

#------------------------------------------------
# Authentication Controller
#------------------------------------------------
class Auth(http.Controller):

    def auth_info(self,message, status,api_key = None,):
        request.session.ensure_valid()

        data = {
            # "description": "Successful = 0, Error = 1, Invalid Value = 2",

            "returncode":status,
            "message": message,
            "data":{
                # "session_id": request.session_id,
                "uid": request.session.uid,
                "user_context": request.session.get_context() if request.session.uid else {},
                # "db": request.session.db,
                "login": request.session.login,
                "company_id": request.env.user.company_id.id if request.session.uid else None,
                # "partner_id": request.env.user.partner_id.id if request.session.uid and request.env.user.partner_id else None,
                "partner_id": request.env.user.partner_id.id if request.session.uid and request.env.user.partner_id else None,
            }

        }
        if api_key is not None:
            data['data']['api_key'] = api_key
        return data

    def make_response(self, message, status, api_key = None):
        data = {
            "jsonrpc": "2.0",
            "result": self.auth_info(message, status, api_key)
        }
        return request.make_response(json.dumps(data), headers=[('Content-Type','application/json')], cookies=None)

    def generate_api_key(self, uid):
        Model = request.env['authtoken.authtoken']
        record = Model.sudo().search([('user_id','=', uid)])
        api_key = request.csrf_token()
        end_time = datetime.datetime.now() + datetime.timedelta(days = 1)

        if not record.exists():

            record = Model.sudo().create({'api_key': api_key,'user_id': uid , 'end_time': end_time})
        else:
            record.write({'api_key':api_key, 'end_time': end_time})

        return api_key

    def get_api_key(self, uid):
        Model = request.env['authtoken.authtoken']
        record = Model.sudo().search([('user_id','=', uid)])

        if record:
            return record.api_key
        return False


    ## generate api
    # def register_info(self,description,message,uid,db):
    #     data = {
    #         "description":description,
    #         "message": message,
    #         "user_id": uid,
    #         "db_name": db,
    #     }
    #
    #     return data
    #
    # def find_db(self,login):
    #     uid = request.env['res.users'].sudo().search([('login','=',login)])[0].id
    #     db = request.env['register.register'].sudo().search([('user_id','=',uid)])[0].name_db
    #
    #     return db


    ## regisyter
    # @http.route('/api/register/', type='json', auth='none')
    # def register(self,uid, db):
    #     Model = request.env['register.register']
    #     record = Model.sudo().search([('name_db','=',db)])
    #     if not record.exists():
    #         record = Model.sudo().create({'user_id' : uid,'db_name' :db})
    #         description = "Successful = 1, Error = 0"
    #         message = "Register Successed"
    #         return self.register_info(description,message,uid,db)
    #     else:
    #         return self.register_info("Successful = 0, Error = 1","DB da su dung")

    @http.route('/api/auth_info', methods=['GET'], auth='none')
    def get_auth_info(self):
        api_key = self.get_api_key(request.session.uid)

        if api_key:
            return self.make_response("Susccesful: get user info", 200, api_key)
        return self.make_response("ERROR: api_key is not exists", 101)


    @http.route('/api/login', type='json', auth='none')
    def login(self,login, password, base_location=None):
        db = login
        request.session.authenticate(db, login, password)
        if request.session.uid:
            api_key = self.generate_api_key(request.session.uid)
            message="login success"
            status = 200
            # return self.auth_info("Sign in: successful", 0 , api_key)
            return self.auth_info(message, status, api_key)
        else:
            message = "Incorrect username or password"
            status = 81
            return self.auth_info(message, status)
            # return self.auth_info("Login Fail", 1)

    ## login withought db
    # @http.route('/api/login_res', type='json', auth='none')
    # def login_res(self,login,password,base_location=None):
    #     db = self.find_db(login)
    #     request.session.authenticate(db,login,password)
    #
    #     if request.session.uid:
    #         api_key = self.generate_api_key(request.session.uid)
    #         return self.auth_info("Sign in: successful", 0, api_key)
    #     else:
    #         return self.auth_info("Login Fail", 1)


    @http.route('/api/change_password', type='json', auth='user')
    def change_password(self, fields):
        old_password, new_password,confirm_password = operator.itemgetter('old_pwd', 'new_password','confirm_pwd')(
                dict(map(operator.itemgetter('name', 'value'), fields)))
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error':_('You cannot leave any password empty.'),'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),'title': _('Change Password')}
        try:
            if request.session.model('res.users').change_password(
                old_password, new_password):
                return {'returncode':200,'message':'Change password suscess','data':{'login': request.session.login ,'new_password':new_password }}
        except Exception:
            return {'returncode':420 ,'error': _('The old password you provided is incorrect, your password was not changed.'), 'title': _('Change Password')}
        return {'returncode':503 ,'error': _('Error, password not changed !'), 'title': _('Change Password')}

    @http.route('/api/logout', type='json', auth='user')
    def logout(self):
        request.session.logout()
        return {"returncode":200,"message":"Sign Out: Successful"}
