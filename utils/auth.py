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

def add_post(username, image_url, thumb_url):
    session = Session()
    print(username)
    user = session.query(User).filter(User.name==username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user_id=user.id)
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()
    return post_id

def get_post(post_id):
    session = Session()
    post = session.query(Post).filter(Post.id==post_id).first()
    print(post.user)
    return post

def get_all_posts(username=None):
    session = Session()
    if username:
        user = session.query(User).filter_by(name=username).first()
        posts = session.query(Post).filter_by(user=user).all()
    else:
        posts = session.query(Post).all()
    if posts:
        return posts
    else:
        return []
