import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers import main, auth

define('port', default="8000", help="Listening Port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/pic", main.ExploreHandler),
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
            (r"/signup", auth.RegisterHandler),
            (r"/login", auth.LoginHandler),
            (r"/logout", auth.LogoutHandler),
        ]
        settings = dict(
            debug=True,
            static_path = "static",
            template_path = "templates",
            # static_url_prefix = "/photo/"    修改静态目录名称
            cookie_secret = "jsahcaskljcasoicjasxklasmc",
            xsrf_cookies = True,
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
