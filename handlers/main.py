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
        page_num = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '8'))
        posts = self.orm.get_all_posts()
        pg = self.orm.get_pg(page_num, page_size)
        page_list = self.orm.get_page_list(page_num, page_size)
        count_list = [self.orm.get_like_count(post.id) for post in posts]
        like_list = [self.orm.post_is_like(self.current_user, post.id) for post in posts]
        return self.render("index.html", posts=pg.items,
                           pg=pg,
                           page_num=page_num,
                           page_list=page_list,
                           page_size=page_size,
                           count_list=count_list,
                           like_list=like_list)


class MyselfHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_all_posts(self.current_user)
        count_list = [self.orm.get_like_count(post.id) for post in posts]
        like_list = [self.orm.post_is_like(self.current_user, post.id) for post in posts]
        self.render("index.html", posts=posts,
                    like_list=like_list,
                    count_list=count_list)


class ExploreHandler(BaseHandler):
    def get(self):
        posts = self.orm.get_all_posts()
        return self.render("explore.html", posts=posts)


class PostHandler(BaseHandler):
    def get(self, post_id):
        post = self.orm.get_post(int(post_id))
        if post:
            count = self.orm.get_like_count(post.id)
            like = self.orm.post_is_like(self.current_user, post.id)
            self.render("post.html", post=post, count=count, like=like)
        else:
            self.render("404notfound.html")


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


class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        query_name = self.get_argument('name', '')
        if query_name:
            name = query_name
        else:
            name = self.current_user
        user = self.orm.get_user(name)
        posts = self.orm.get_all_posts(name)
        like_posts = self.orm.get_like_post(name)
        self.render('profile.html', user=user, posts=posts, like_posts=like_posts)


class AddLikeHandler(BaseHandler):
    def post(self):
        post_id = self.get_argument("post_id", '')
        is_like = self.get_argument("is_like", '')
        user = self.orm.get_user(self.current_user)
        self.orm.add_or_cut_like(user_id=user.id, post_id=int(post_id), is_like=is_like)
        like_count = self.orm.get_like_count(int(post_id))
        self.write({
            'id': post_id,
            'count': like_count
        })