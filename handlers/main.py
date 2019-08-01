import tornado.web
import os
from PIL import Image
from pycket.session import SessionMixin
from utils.auth import add_post, get_post, get_all_posts
from utils.photo import UploadImage


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get("tudo_cookie")

class IndexHandler(BaseHandler):
    def get(self):
        posts = get_all_posts()
        return self.render("index.html", posts=posts)


class ExploreHandler(BaseHandler):
    def get(self):
        posts = get_all_posts()
        return self.render("explore.html", posts=posts)

class PostHandler(BaseHandler):
    def get(self, post_id):
        post = get_post(post_id)
        if post:
            return self.render("post.html", post=post)
        else:
            return self.send_error(404)

class UploadHandler(BaseHandler):
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
            post_id = add_post(upload_img.get_image_path, self.current_user)
        if post_id:
            self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('upload error')
