from openerp import http
from openerp.http import request
import json

class JsonHelper(http.Controller):
    @staticmethod
    def make_jsonresponse(message, status, items = None):
        data = {
            "jsonrpc": "2.0",
            "result": JsonHelper.make_jsondata(message, status, items)
        }
        return request.make_response(json.dumps(data), headers=[('Content-Type','application/json')], cookies=None)
    
    @staticmethod
    def make_jsondata(message, status, items = None):
        data = {
            "message": message,
            "status": status
        }
        if items is not None:
            data['items'] = items;
            data['length'] = len(items)
        return data