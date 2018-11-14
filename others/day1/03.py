# coding: utf-8
import datetime
import json
import os
from itertools import izip
from json import JSONEncoder

import MySQLdb
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler


def dictfetchall(cursor, strip_field_pre=False):
    """
    Returns all rows from a cursor as a dict
    """
    desc = cursor.description
    if strip_field_pre:
        return [
            dict(izip([col[0][2:] for col in desc], row))
            for row in cursor.fetchall()
        ]

    return [
        dict(izip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class CusJSONEncoder(JSONEncoder):
    """
    盛天小贷对接专用JSON序列化
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return int(obj.strftime('%Y%m%d'))
        else:
            return super(CusJSONEncoder, self).default(obj)


class IndexHandler(RequestHandler):

    def initialize(self, name):
        self.name = name

    def get(self, *args, **kwargs):
        resp = {
            "name": "hello",
            "age": 18,
            "sex": u"男"
        }
        cursor = self.application.cursor
        sql = "select * from auth_user where username='%s'" % self.name
        cursor.execute(sql)
        res = dictfetchall(cursor)
        if res:
            hehe = json.dumps(res, cls=CusJSONEncoder)
        else:
            hehe = dict()

        # cursor.close()
        # self.application.db.close()

        self.write(hehe)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler, {"name": "admin"})
        ]

        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "statics"),
                        debug=True,
                        )
        super(Application, self).__init__(handlers, **settings)

        #TODO 创建一个全局的mysql连接示例供handler使用，这里释放如何处理

        self.db = MySQLdb.connect("127.0.0.1", "root", "", "polls")
        self.cursor = self.db.cursor()


application = Application()

if __name__ == '__main__':
    application.listen(9985)
    tornado.ioloop.IOLoop.current().start()
