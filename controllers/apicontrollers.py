from openerp import http,models
from openerp.http import request
from openerp.exceptions import AccessError, MissingError, ValidationError, UserError
from jsonhelper import JsonHelper
import json
import logging
import datetime
import re
#------------------------------------------------
# API Helper
#------------------------------------------------
def get_object(name):
    DBObject = http.request.env['dbobject.dbobject']
    Objects = DBObject.sudo().search([('name','=', name)])
    return Objects 
def string_to_fields(values):
    return [value.strip() for value in (values.split(',') if values else '')]
def string_to_domain(values):
    return []
def string_to_sort(values):
    return []
def string_to_group(values):
    return [value.strip() for value in re.split(': |, |\*|\n', values)]    #string -> []
def verify_api_key(api_key):
    uid = request.session.uid
    Model = request.env['authtoken.authtoken']
    record = Model.sudo().search([('user_id', '=', uid)])
    if not record.exists() or api_key is None:
        return False
    if api_key == record.api_key and record.active:
        return True
    return False
        
#------------------------------------------------
# API Controller
#------------------------------------------------
class Api(http.Controller):
    #
    def do_search_read(self, model, fields=False, offset=0, limit=False, domain=None
                       , sort=None):
        Model = request.session.model(model)
        # search model theo domain return json
        records = Model.search_read(domain, fields, offset or 0, limit or False, sort or False,request.context)
        return records
        
    def do_search_read_group(self, model, fields=False, offset=0, limit=False, domain=None, sort=None, groupby=None):
        Model = request.env[model]
        records = Model.search(domain)
        
        group = string_to_group(groupby)
        if group[0] not in records._columns:
            return self.do_search_read(model, fields, offset, limit, domain,sort)
        s = set(dic[group[0]] for dic in records)
        if len(s) == 0:
            return self.do_search_read(model, fields, offset, limit, domain,sort)
        result = []
        for x in s:
            if isinstance(x, models.Model):
                name = x.id
                value ={group[0]: x.id}
                for v in group:
                    if group.index(v) != 0:
                        value[v] = x[v]
            else:
                name = x
                value = {group[0]: x}
            do = domain[:]
            do.append([group[0], '=', name])
            data = self.do_search_read(model, fields, offset, limit, do, sort)
            value['list'] = data
            result.append(value)       
        return result
        
    @http.route('/api/search_read', type='json', auth="public")
    def search_read(self, model, fields=False, offset=0, limit=False, domain=None, sort=None, groupby=None, api_key=None):
        try:
            if not verify_api_key(api_key):
                return JsonHelper.make_jsondata("AccessError: Verify your api_key", 1)    
            if groupby:
                return self.do_search_read_group(model, fields, offset,limit, domain, sort, groupby)
            return JsonHelper.make_jsondata("Sucessful", 0, self.do_search_read(model, fields, offset, limit, domain, sort))
        except AccessError:
            return JsonHelper.make_jsondata("AccessError: You don't have permission to get data", 1)
        except:
            return JsonHelper.make_jsondata("ValidationError: ... ", 2)
    @http.route(['/api/db/<tname>','/api/db/<tname>/<int:id>'], auth='public', methods=['GET'])
    def get(self, tname,id=None, api_key=None):
        try:
            if not verify_api_key(api_key):
                return JsonHelper.make_jsonresponse("AccessError: Verify your api_key", 1)
            Objects = get_object(tname)
            if not Objects:
                return JsonHelper.make_jsonresponse("Invalid URL", 1)
            
            model = Objects.model
            fields = string_to_fields(Objects.field)
            offset = Objects.offset
            limit = Objects.limit
            domain = string_to_domain(Objects.domain)
            if id:
                domain.append(['id','=', id])
            sort = string_to_sort(Objects.sort)
            
            if Objects.groupby is not False:
                return JsonHelper.make_jsonresponse("Sucessful", 0, self.do_search_read_group(model, fields, offset,limit, domain, sort, Objects.groupby))
            else:
                return JsonHelper.make_jsonresponse("Sucessful", 0, self.do_search_read(model, fields, offset, limit, domain, sort))
        except :
            return JsonHelper.make_jsonresponse("AccessError: You don't have permission to get data", 1)
        
    @http.route('/api/db/<tname>', auth='public', methods=['POST'], type='json')
    def create(self, tname, record, api_key=None):
        logging.warning("assssssssssss")
        try:
            if not verify_api_key(api_key):
                return JsonHelper.make_jsondata("AccessError: Verify your api_key", 1)
            Objects = get_object(tname)
            if not Objects:
                return JsonHelper.make_jsondata("Invalid URL", 1)
            logging.warning("vvvvvvvvvvvvvvvvvvvvvv")
            logging.warning(record['value_ids'])
            # if(tname == )
            record['value_ids'] = [(4,record['value_ids'],0)]
            # record['value_ids'] = json.dumps(record['value_ids'])
            logging.warning(record['value_ids'])

            Model = request.session.model(Objects.model)
            model = Model.create(record)
            return JsonHelper.make_jsondata("Create Successful", 0) 
        except ValueError:
            logging.warning(ValueError)
            return JsonHelper.make_jsondata("AccessError: You dont' have permission to create a record!", 1)
        
        
    @http.route('/api/db/<tname>/<int:id>',auth='public', methods=['PUT','DELETE'], type='json')
    def update_delete(self, tname, id, record=None,api_key=None):
        try:
            if not verify_api_key(api_key):
                return JsonHelper.make_jsondata("AccessError: Verify your api_key", 1)
            Objects = get_object(tname)
            if not Objects:
                return JsonHelper.make_jsondata("Invalid URL",1)
            
            Model = request.session.model(Objects.model)
            model = Model.browse([id])
            if not model.exists():
                return JsonHelper.make_jsondata("Record id = " + str(id) +" is not exists", 1)
            if request.httprequest.method == 'PUT':
                model.write(record)
                return JsonHelper.make_jsondata("UPDATE Successful",0)
            if request.httprequest.method == 'DELETE':
                model.unlink()
                return JsonHelper.make_jsondata("DELETE Successful",0)
                
        except:
            return JsonHelper.make_jsondata("AccessError: You dont' have permission to update a record!",1)
        
    @http.route('/api/fields/<tname>/', auth='public', methods=['GET'])
    def get_fields(self, tname, api_key=None):

        try:
            if not verify_api_key(api_key):
                return JsonHelper.make_jsonresponse("AccessError: Verify your api_key", 1)
            Objects = get_object(tname)
            if not Objects:
                return JsonHelper.make_jsondata("Invalid URL",1)
            
            Model = request.env[Objects.model]
            record = Model.fields_get([])
            return JsonHelper.make_jsonresponse("Sucessful", 0, record)
        except:
            return JsonHelper.make_jsondata("AccessError: You dont' have permission to get fields of record!",1)
        
        