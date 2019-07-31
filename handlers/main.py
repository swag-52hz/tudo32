import tornado.web
from PIL import Image
from pycket.session import SessionMixin
from utils.auth import add_post, get_post, get_all_posts


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get("tudo_cookie")

class IndexHandler(BaseHandler):
    def get(self):
        posts = get_all_posts()
        return self.render("index.html", posts=posts)


class ExploreHandler(BaseHandler):
    def get(self):
        return self.render("explore.html", img_list=[])

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
        file_dict = file_list[0]
        file_name = file_dict["filename"]
        img_path = 'static/images/{}'.format(file_name)
        with open(img_path, 'wb') as f:
            f.write(file_dict["body"])
        img = Image.open(img_path)
        img.thumbnail((200, 200))   # 生成缩略图
        img.save('static/images/thumb_{}'.format(file_name))
        post_id = add_post('images/{}'.format(file_name), self.current_user)
        if post_id:
            self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('upload error')
