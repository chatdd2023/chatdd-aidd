import tornado.ioloop
import tornado.web
from tornado.gen import coroutine

'''
  功能：构建tornado web 服务
  author:boge
  date:2023-11-26
'''

class AsyncHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        yield tornado.gen.sleep(2)
        self.write("Async request complete!")

def make_app():
    return tornado.web.Application([
        (r"/async", AsyncHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()
