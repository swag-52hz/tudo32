from hashlib import md5
from models.auth import User, Session


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


