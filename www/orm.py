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

