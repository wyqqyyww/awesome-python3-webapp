__author__ = 'wuxq'

import aiomysql
import asyncio,logging

import baseDao

def log(sql,args=()):
    logging.info('sql: %s'%sql,',args: %s'%args)

class ModelMetaclass(type):
    pass


class Model(dict,metaclass=ModelMetaclass):
    def __init__(self,**kwargs):
        super(Model,self).__init__(**kwargs)

    def __getattr__(self, key):

        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'"%key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self,key):
        return getattr(self,key,None)

    def getValueOrDefault(self,key):
        pass

class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return "<%s,s%:s%>"%(self.__class__.__name__,self.column_type,self.name)

class StringField(Field):
    def __init__(self,name,ddl='varchar(100)',primary_key=False,default=None):
        return super.__init__(name,ddl,primary_key,default)

class FloatField(Field):
    def __init__(self,name,ddl='float(20)',primary_key=False,default=None):
        return super.__init__(name,ddl,primary_key,default)

class TextField(Field):
    def __init__(self,name,ddl='text(1000)',primary_key=False,default=None):
        return super.__init__(name,ddl,primary_key,default)

class BooleanField(Field):
    def __init__(self,name,ddl='boolean',primary_key=False,default=True):
        return super.__init__(name,ddl,primary_key,default)