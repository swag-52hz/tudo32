from hashlib import md5
from models.auth import User, Post, Session


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
        print(post.user)
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

    def add_post(self, username, image_url, thumb_url):
        user = self.get_user(username)
        post = Post(image_url=image_url, thumb_url=thumb_url, user_id=user.id)
        self.db.add(post)
        self.db.commit()
        post_id = post.id
        return post_id
