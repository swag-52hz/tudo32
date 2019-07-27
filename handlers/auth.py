from .main import BaseHandler
from utils.auth import register


class RegisterHandler(BaseHandler):
    def get(self):
        msg = self.get_argument('msg', '')
        return self.render('register.html', msg=msg, next_url='/')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        password_repeat = self.get_argument('password_repeat', '')
        if username and password and password_repeat:
            if password == password_repeat:
                ret = register(username, password)
                if ret:
                    self.session.set('tudo_cookie', username)
                    self.redirect('/')
                else:
                    msg = 'register failed'
            else:
                msg = 'password is different'
        else:
            msg = 'username or password is empty'
        return self.redirect('/signup?msg={}'.format(msg))