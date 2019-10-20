import tornado.web
import os
from pycket.session import SessionMixin
from utils.auth import HandlerORM
from models.auth import Session
from utils.photo import UploadImage


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get("tudo_cookie")

    def prepare(self):
        self.db_session = Session()
        self.orm = HandlerORM(self.db_session)

    def on_finish(self):
        self.db_session.close()


class IndexHandler(BaseHandler):
    def get(self):
        posts = self.orm.get_all_posts()
        return self.render("index.html", posts=posts)


class MyselfHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_all_posts(self.current_user)
        return self.render("index.html", posts=posts)


class ExploreHandler(BaseHandler):
    def get(self):
        posts = self.orm.get_all_posts()
        return self.render("explore.html", posts=posts)


class PostHandler(BaseHandler):
    def get(self, post_id):
        post = self.orm.get_post(int(post_id))
        if post:
            return self.render("post.html", post=post)
        else:
            return self.send_error(404)


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("upload.html")

    def post(self):
        file_list = self.request.files.get("picture")
        post_id = None
        for file_dict in file_list:
            file_name = file_dict["filename"]
            _, ext_name = os.path.splitext(file_name)
            upload_img = UploadImage(ext_name, self.application.settings['static_path'])
            upload_img.save_content(file_dict["body"])
            upload_img.save_thumb_img()
            post_id = self.orm.add_post(self.current_user, upload_img.get_image_path, upload_img.get_thumb_url)
        if post_id:
            self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('upload error')
