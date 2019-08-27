import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.web import URLSpec

from handlers import main, auth, chat, service

define('port', default="8000", help="Listening Port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/myself", main.MyselfHandler),
            (r"/pic", main.ExploreHandler),
            URLSpec(r"/post/(?P<post_id>[0-9]+)", main.PostHandler, name='post'),
            (r"/signup", auth.RegisterHandler),
            (r"/login", auth.LoginHandler),
            (r"/logout", auth.LogoutHandler),
            (r"/upload", main.UploadHandler),
            (r"/ws", chat.ChatWSHandler),
            (r"/room", chat.ChatRoomHandler),
            (r"/sync", service.SyncHandler),
            (r"/save", service.AsyncHandler),
        ]
        settings = dict(
            debug=True,
            static_path = "static",
            template_path = "templates",
            # static_url_prefix = "/photo/"    修改静态目录名称
            cookie_secret = "jsahcaskljcasoicjasxklasmc",
            # xsrf_cookies = True,  开启xsrf验证
            login_url = "/login",
            pycket = {
                'engine': 'redis',
                'storage':{
                    'host': 'localhost',
                    'port': 6379,
                    # 'passsword': ''
                    'db_sessions': 5,
                    'max_connections': 2**30,
                },
                'cookies':{
                    'expires_days': 30,
                }
            }
        )
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
