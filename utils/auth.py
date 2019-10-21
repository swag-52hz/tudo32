from hashlib import md5
from models.auth import User, Post, Session, LikePost
from sqlalchemy_pagination import paginate
from sqlalchemy.sql import and_, exists


SALT = "tudopass"


def hash(password):
    return md5("{}{}".format(password, SALT).encode()).hexdigest()


def register(username, password, password_repeat):
    ret = {
        'msg': 'other error'
    }
    if username and password and password_repeat:
        if password == password_repeat:
            s = Session()
            user = s.query(User).filter_by(name=username).all()
            if user:
                msg = 'username is already exists'
            else:
                new_user = User(name=username, password=hash(password))
                s.add(new_user)
                s.commit()
                s.close()
                msg = 'ok'
        else:
            msg = 'password is different'
    else:
        msg = 'username or password is empty'
    ret['msg'] = msg
    return ret


def authenticate(username, password):
    ret = {}
    if username and password:
        result = User.is_exists(username, hash(password))
        if result:
            ret['msg'] = 'ok'
        else:
            ret['msg'] = 'username or password error'
    else:
        ret['msg'] = 'username or password is empty'
    return ret


class HandlerORM:
    """在RequestHandler实例化查询的Session,然后配合使用来操作数据库"""
    def __init__(self, db_session):
        self.db = db_session

    def get_user(self, username):
        user = self.db.query(User).filter(User.name == username).first()
        if user:
            return user
        else:
            return None

    def get_post(self, post_id):
        """
        返回指定id的图片
        :param post_id: 图片id
        :return:
        """
        post = self.db.query(Post).filter(Post.id == post_id).first()
        return post

    def get_all_posts(self, username=None):
        """
        查询获取所有照片或者是特定用户的照片
        :param username:如果没有，就是获取全部照片
        :return:
        """
        if username:
            user = self.get_user(username)
            posts = self.db.query(Post).filter_by(user=user).all()
        else:
            posts = self.db.query(Post).all()
        if posts:
            return posts
        else:
            return []

    def get_pg(self, page=1, page_size=8, username=None):
        """获取分页对象"""
        if username:
            user = self.get_user(username)
            qs = self.db.query(Post).filter_by(user=user)
        else:
            qs = self.db.query(Post)
        pg = paginate(qs, page, page_size)
        return pg

    def get_page_list(self, page, page_size):
        """获取页码列表"""
        num = 3     # 显示的页数，一定是个奇数
        pg = self.get_pg(page, page_size)
        page_num = page         # 当前页码
        # total_num = pg.total    # 图片总数
        total_page = pg.pages   # 总共的页数
        page_list = []
        if page_num - (num - 1) // 2 <= 0:  # 显示左边的页码以及当前页码
            for i in range(page_num):
                page_list.append(i + 1)
        else:  # 说明当前页码足够大
            for i in range(page_num - (num - 1) // 2, page_num + 1):
                page_list.append(i)
        if page_num + (num - 1) / 2 >= total_page:
            for i in range(page_num + 1, total_page + 1):
                page_list.append(i)
        else:
            for i in range(page_num + 1, page_num + (num - 1) // 2 + 1):
                page_list.append(i)
        return page_list


    def add_post(self, username, image_url, thumb_url):
        user = self.get_user(username)
        post = Post(image_url=image_url, thumb_url=thumb_url, user_id=user.id)
        self.db.add(post)
        self.db.commit()
        post_id = post.id
        return post_id

    def get_like_post(self, username):
        """
        获取用户喜欢的图片列表
        :param username: 根据用户名进行查找
        :return:
        """
        user = self.get_user(username)
        like_posts = self.db.query(Post).filter(Post.id == LikePost.post_id,
                                       LikePost.user_id == user.id).all()
        return like_posts

    def get_like_count(self, post_id):
        count = self.db.query(LikePost).filter_by(post_id=post_id).count()
        return count

    def add_or_cut_like(self, user_id, post_id, is_like):
        like_post = LikePost(user_id=user_id, post_id=post_id)
        if is_like == "true":
            self.db.query(LikePost).filter(LikePost.user_id == user_id, LikePost.post_id == post_id).delete()
        else:
            self.db.add(like_post)
        self.db.commit()

    def post_is_like(self, username, post_id):
        user = self.get_user(username)
        res = self.db.query(exists().where(and_(LikePost.user_id == user.id,
                                                LikePost.post_id == post_id))).scalar()
        return res
