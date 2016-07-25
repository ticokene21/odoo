# # -*- coding: utf-8 -*-
# from openerp import http,models
# import json
# import datetime
# import requests
# from openerp.exceptions import AccessError, MissingError, ValidationError, UserError
#
# # ----------------------------------------------
# # API Helper
# # ----------------------------------------------
#
# # def verify_api_key(api_key):
# #     Models = http.request.env['authtoken.authtoken']
# #     model = Models.sudo().search([('api_key','=',api_key)])
# #     if len(model) > 0:
# #         if model.active == True:
# #             return model.user_id;
# #     return -1
#
#
# # def json_respone(description, message, status, result):
# #     data = json_data (description, message, status,result)
# #     return http.request.make_response(json.dumps(data), headers=[('Content-Type','application/json')], cookies=None)
#
#
# # def json_data (description, message, status, result):
# #     data = {
# #         "description": description,
# #         "status": status,
# #         "message": message,
# #         "result" : result
# #     }
# #     return data
#
# # def search_data(name, uid, domains, fields, limit, groupby):
# #     Models = http.request.env[name]
# #     model = Models.sudo(uid).search(domains)
# #     group = str(groupby).split(':')
# #     if len(group) > 1:
# #         att = group[1].split(',')
#
# #     if group[0].strip() not in model._columns:
# #         return Models.sudo(uid).search_read(domains, fields, limit=limit)
#
# #     s = set(dic[group[0].strip()]  for dic in model)
# #     if len(s) == 0:
# #         return Models.sudo(uid).search_read(domains, fields, limit=limit)
#
# #     result = []
# #     for x in s:
# #         if isinstance(x,models.Model):
# #             name = x.id
# #             value = {group[0].strip(): x.id}
# #             if len(group) > 1:
# #                 for v in att:
# #                     if v.strip() in x._columns:
# #                         value[v.strip()] = x[v.strip()]
# #         else:
# #             name = x
# #             value = {group[0].strip(): x}
#
# #         domain = domains[:]
# #         domain.append([group[0].strip() ,'=', name])
# #         data = Models.sudo(uid).search_read(domain,fields, limit=limit)
# #         value['items'] = data
# #         result.append(value)
# #     return result
#
# # ----------------------------------------------
# # API Controller
# # ----------------------------------------------
# class ApiController(http.Controller):
#
#     # # Authentication
#     # # ['POST'] /api/common/
#     # # Executes the login and returns the authentication token
#     # @http.route('/api/common/', auth='user', methods=['GET'], csrf=False)
#     # def common(self, **kw):
#     #     Models = http.request.env['authtoken.authtoken']
#     #     user = http.request.env.user
#     #     api_key = http.request.csrf_token()
#     #     end_time = datetime.datetime.now() + datetime.timedelta(days=1)
#
#
#     #     model = Models.sudo().search([('user_id','=', user.id)])
#     #     if len(model) > 0:
#     #         # return access_token if it's already active
#     #         if model.active == True:
#     #             return json_respone("PASS: 0, FAIL: 1", "OK Old", 0, model._to_json())
#     #         else:
#     #         # renew
#     #             model.write({'api_key':api_key, 'end_time': end_time})
#     #             return json_respone("PASS: 0, FAIL: 1", "OK Renew", 0, model._to_json())
#
#     #     # Create new access_token
#     #     model = Models.sudo().create({'api_key': api_key,'user_id':user.id , 'end_time': end_time})
#     #     return json_respone("PASS: 0, FAIL: 1", "OK New", 0, model._to_json())
#     #     # return model._to_json('New', 0)
#
#
#
#     # # Databases
#     # # ['GET'] /api/DB/
#     # # Returns a list of all existing databases
#     # @http.route('/api/DB/', auth='public', methods=['GET'], csrf=False)
#     # def db(self, **kw):
#     #     if 'api_key' not in kw:
#     #         return json_respone("PASS: 0, FAIL: 1", "api_key missing", 1, '')
#     #     uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_respone("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#     #     try:
#     #         DBObject = http.request.env['dbobject.dbobject']
#     #         Objects = DBObject.sudo(uid).search_read([], ['name', 'tname'])
#     #     except AccessError:
#     #         return json_respone("PASS: 0, FAIL: 1", "AccessError: You don't have permission to get a info!", 1, '')
#     #     return json_respone("PASS: 0, FAIL: 1", "Successfully", 0, Objects)
#
#
#     # # Records
#     # # ['GET'] /api/DB/<Tname>/
#     # # get all
#     # @http.route('/api/DB/<Tname>/', auth='public', methods=['GET'], csrf=False)
#     # def getall(self, Tname, **kw):
#     #     if 'api_key' not in kw:
#     #         uid = 9
#     #     else:
#     #         uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_respone("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#
#     #     DBObject = http.request.env['dbobject.dbobject']
#     #     object = DBObject.sudo(uid).search([('name','=', Tname)])
#     #     if len(object) == 0:
#     #         return json_respone("PASS: 0, FAIL: 1", "Can't find the object", 1, '')
#     #     try:
#     #         model = search_data(object.tname, uid, domains=[],fields=[x.strip() for x in (object.att.split(',') if object.att else '')] , limit=object.limit, groupby=object.groupby)
#     #     except AccessError:
#     #         return json_respone("PASS: 0, FAIL: 1", "AccessError: You don't have permission to get a record!", 1, '')
#     #     return json_respone("PASS: 0, FAIL: 1", "Sucessfully", 0, model)
#
#     # # ['GET'] /api/DB/<Tname>/<int:id>
#     # # Performs a search in a table for the specified id and returns the founded records with the speciafied fields
#     # @http.route('/api/DB/<Tname>/<int:id>', auth='public', methods=['GET'], csrf=False)
#     # def get(self, Tname, id, **kw):
#     #     if 'api_key' not in kw:
#     #         uid = 9
#     #     else:
#     #         uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_respone("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#
#     #     DBObject = http.request.env['dbobject.dbobject']
#     #     object = DBObject.sudo(uid).search([('name','=', Tname)])
#     #     if len(object) == 0:
#     #         return json_respone("PASS: 0, FAIL: 1", "Can't find the object", 1, '')
#     #     try:
#     #         model = search_data(object.tname, uid, domains=[('id','=', id)],fields=[x.strip() for x in (object.att.split(',') if object.att else '')], limit=object.limit, groupby=object.groupby)
#     #     except AccessError:
#     #         return json_respone("PASS: 0, FAIL: 1", "AccessError: You don't have permission to get a record!", 1, '')
#     #     return json_respone("PASS: 0, FAIL: 1", "Sucessfully", 0, model)
#
#     # # ['POST'] /api/DB/<Tname>/
#     # # Inserts a new record into a table
#     # @http.route('/api/DB/<Tname>/', auth='public', methods=['POST'], csrf=False, type='json')
#     # def create(self, Tname, **kw):
#     #     if 'api_key' not in kw:
#     #         return json_data("PASS: 0, FAIL: 1", "api_key missing", 1, '')
#
#     #     uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_data("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#     #     if 'record' not in kw:
#     #         return json_data("PASS: 0, FAIL: 1", "Can't find record field in json input", 1, '')
#
#     #     DBObject = http.request.env['dbobject.dbobject']
#     #     object = DBObject.sudo().search([('name','=', Tname)])
#     #     if len(object) == 0:
#     #         return "Can't Find Object"
#     #     try:
#     #         Models = http.request.env[object.tname]
#     #         model = Models.sudo(uid).create(kw['record'])
#     #     except AccessError:
#     #         return json_data("PASS: 0, FAIL: 1", "AccessError: You don't have permission to create new record!", 1, '')
#     #     return json_data("PASS: 0, FAIL: 1", "CREATE Sucessfully", 0, {"id": model.id} )
#
#
#
#     # # ['PUT'] /api/DB/<Tname>/<int:id>
#     # # Updates for a record with the specified id
#     # @http.route('/api/DB/<Tname>/<int:id>/', auth='public', methods=['PUT'], csrf=False,type='json')
#     # def update(self, Tname, id, **kw):
#     #     if 'api_key' not in kw:
#     #         return json_data("PASS: 0, FAIL: 1", "api_key missing", 1, '')
#
#     #     uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_data("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#     #     if 'record' not in kw:
#     #         return json_data("PASS: 0, FAIL: 1", "Can't find record field in json input", 1, '')
#
#     #     DBObject = http.request.env['dbobject.dbobject']
#     #     object = DBObject.sudo(uid).search([('name','=', Tname)])
#     #     if len(object) == 0:
#     #         return json_data("PASS: 0, FAIL: 1", "Can't find the object", 1, '')
#     #     try:
#     #         Models = http.request.env[object.tname]
#     #         model = Models.sudo(uid).browse([id])
#     #         if not model.exists():
#     #             return json_data("PASS:0, FAIL: 1", "model is not exists", 1 , '')
#
#     #         model.write(kw['record'])
#     #     except AccessError:
#     #         return json_data("PASS: 0, FAIL: 1", "AccessError: You don't have permission to update new record!", 1, '')
#     #     return json_data("PASS: 0, FAIL: 1", "UPDATE SUCESSFULLY",0 , '')
#
#     # # ['DELETE'] /api/DB/<Tname>/<int:id>
#     # # Deletes a record with the specified id from table
#     # @http.route('/api/DB/<Tname>/<int:id>/', auth='public', methods=['DELETE'], csrf=False, type='json')
#     # def delete(self, Tname, id, **kw):
#     #     if 'api_key' not in kw:
#     #         return json_data("PASS: 0, FAIL: 1", "api_key missing", 1, '')
#
#     #     uid = verify_api_key(kw['api_key'])
#     #     if uid == -1:
#     #         return json_data("PASS: 0, FAIL: 1", "Authentication Fails", 1, '')
#
#
#     #     DBObject = http.request.env['dbobject.dbobject']
#     #     object = DBObject.sudo(uid).search([('name','=', Tname)])
#     #     if len(object) == 0:
#     #         return json_data("PASS: 0, FAIL: 1", "Can't find the object", 1, '')
#     #     try:
#     #         Models = http.request.env[object.tname]
#     #         model = Models.sudo(uid).browse([id])
#     #         if not model.exists():
#     #             return json_data("PASS:0, FAIL: 1", "model is not exists", 1 , '')
#     #         model.unlink()
#     #     except AccessError:
#     #         return json_data("PASS: 0, FAIL: 1", "AccessError: You don't have permission to detele new record!", 1, '')
#     #     except:
#     #         return json_data("PASS: 0, FAIL: 1", "You cannot delete a product saleable in point of sale while a session is still opened.", 1, '')
#     #     return json_data("PASS: 0, FAIL: 1", "DELETE SUCESSFULLY",0 , '')
#
#
#
#
#
