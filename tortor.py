import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class AnnounceHandler(tornado.web.RequestHandler):
    def get(self):
        info_hash = self.get_argument('info_hash')
        peer_id = self.get_argument('peer_id')
        self.write(peer_id)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()