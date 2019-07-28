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

        ret = register(username, password, password_repeat)
        if ret['msg'] == 'ok':
            self.session.set('tudo_cookie', username)
            self.redirect('/')
        else:
            return self.redirect('/signup?msg={}'.format(ret['msg']))



