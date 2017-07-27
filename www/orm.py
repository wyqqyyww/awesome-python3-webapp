__author__ = 'wuxq'

import aiomysql
import asyncio,logging

import baseDao

def log(sql,args=()):
    logging.info('sql: %s'%sql,',args: %s'%args)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls,name,bases,attrs)

        tableName = attrs.get('__table__',None) or name

        logging.info('found model:%s'%(name,tableName))

        mappings = dict()
        fields = []
        primaryKey = None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info('found field mapping:%s==>%s'%(k,v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field:%s'%k)
                    primaryKey = k
                else:
                    fields.append(k)

        if not primaryKey:
            raise RuntimeError('Primary key not found...')
        for k in mappings.keys():
            attrs.pop(k)#remove fields

        escaped_fields = list(map(lambda f:'`%s`'%f,fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields

        attrs['__select__'] = 'select `%s`,%s from `%s`'%(primaryKey,','.join(escaped_fields),tableName)
        attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values(%s)'%(tableName,','.join(escaped_fields),
                                                                       primaryKey,create_args_string(len(escaped_fields)+1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName,
                                                                   ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)

        return type.__new__(cls,name,bases,attrs)


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