__author__ = 'wuxq'

import aiomysql
import asyncio, logging


def log(sql, args=()):
    logging.info('sql: %s' % sql, ',args: %s' % args)


@asyncio.coroutine
def create_pool(loop, **kwargs):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kwargs.get('host', 'localhost'),
        port=kwargs.get('port', 3306),
        user=kwargs.get('user', 'csst'),
        password=kwargs.get('password', 'csst'),
        db=kwargs.get('db', 'pytest'),
        charset=kwargs.get('charset', 'utf8'),
        autocommit=kwargs.get('autocommit', 'True'),
        maxsize=kwargs.get('maxsize', 20),
        minsize=kwargs.get('minsize', 5),
        loop=loop
    )


@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool

    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor(aiomysql.DictCursor)
            yield from cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = yield from cur.fetchmany(size)
            else:
                rs = yield from cur.fetchall()
            yield from cur.close()
        except BaseException as e:
            raise

        logging.info('rows returned:%s' % len(rs))
        return rs


@asyncio.coroutine
def execute(sql, args):
    log(sql, args)
    global __pool

    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args or ())
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise

        logging.log('rows affected:%s' % affected)
        return affected

