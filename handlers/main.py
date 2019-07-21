import tornado.web
from pycket.session import SessionMixin


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get("tudo_cookie")

class IndexHandler(BaseHandler):
    def get(self):
        return self.render("index.html")

class ExploreHandler(BaseHandler):
    def get(self):
        return self.render("explore.html", img_list=[])

class PostHandler(BaseHandler):
    def get(self, post_id):
        return self.render("post.html", post_id=post_id)