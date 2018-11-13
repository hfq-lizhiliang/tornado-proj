# coding: utf-8
"""
1、"/python" 通过字典在application传参
2、"/contract/(?P<no>\w+)" 通过正则匹配传参

"""

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler

define("port", default=8007, type=int, help="run server on the given port")


class IndexHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self, *args, **kwargs):
        self.write('hello %s' % self.subject)


class RegularHandler(RequestHandler):
    def get(self, no):
        self.write(u"正则表达式:%s" % no)


app = tornado.web.Application([
    (r"/python", IndexHandler, {"subject": "python"}),
    (r"/contract/(?P<no>\w+)", RegularHandler)
],
    debug=True
)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
