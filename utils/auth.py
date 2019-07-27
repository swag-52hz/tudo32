from hashlib import md5
from models.auth import User, Session


SALT = "tudopass"


def hash(password):
    return md5("{}{}".format(password, SALT).encode()).hexdigest()


def register(username, password):
    ret = {}
    user = User(name=username, password=hash(password))
    s = Session()
    s.add(user)
    s.commit()
    s.close()
    ret['msg'] = 'ok'
    return ret
