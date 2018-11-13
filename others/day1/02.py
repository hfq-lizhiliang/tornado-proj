# coding: utf-8

"""
1、返回json
2、重定向
3、抛出异常

"""

import tornado.ioloop
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port")


class IndexHandler(RequestHandler):

    def initialize(self):
        pass

    def get(self, *args, **kwargs):
        resp = {
            "name": "hello",
            "age": 18,
            "sex": u"男"
        }
        self.write(resp)


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('<form method="post"><input type="submit" value="登陆"></form>')

    def post(self, *args, **kwargs):
        self.redirect("/")


class SendErrorHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("抛出错误信息")
        self.send_error(status_code=400, **dict(title=u"崩溃了", content=u"测试"))

    def write_error(self, status_code, **kwargs):
        """
        要想处理send_error() 方法抛出的异常，需要重写此处方法
        :param status_code:
        :param kwargs:
        :return:
        """
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>错误名：%s</p>" % kwargs["title"])
        self.write(u"<p>错误详情：%s</p>" % kwargs["content"])


app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/send_error", SendErrorHandler),
])

if __name__ == '__main__':
    options.parse_command_line()

    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
