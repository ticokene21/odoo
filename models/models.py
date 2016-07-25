# -*- coding: utf-8 -*-

from openerp import models, fields, api,exceptions

class authtoken(models.Model):
    _name = 'authtoken.authtoken'
    
    user_id = fields.Many2one(comodel_name='res.users',delegate=True, required=True, ondelete='set null')
    api_key = fields.Char(String="Access Token" )
    end_time = fields.Datetime(String="End Time")
    active = fields.Boolean(compute="_active", default=False)

    def _active(self):
        self.active = self.end_time > fields.Datetime.now() 
    
        
class dbobject(models.Model):
    _name = 'dbobject.dbobject'
    
    name = fields.Char()
    model = fields.Char(String="Table name")
    domain = fields.Char()
    field = fields.Char()
    limit = fields.Integer()
    offset = fields.Integer()
    sort = fields.Char()
    groupby = fields.Char()

class register(models.Model):
    _name = 'register.register'

    user_id = fields.Many2one(comodel_name='res.users',delegate=True, required=True, ondelete='set null')
    name_db = fields.Char(String = "Database name")



