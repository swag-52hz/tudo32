from .main import BaseHandler
from utils.auth import register, authenticate


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


class LoginHandler(BaseHandler):
    def get(self):
        msg = self.get_argument('msg', '')
        next_url = self.get_argument('next', '/')
        return self.render('login.html', msg=msg, next_url=next_url)

    def post(self):
        username = self.get_argument('name', '')
        password = self.get_argument('password', '')
        ret = authenticate(username, password)
        if ret['msg'] == 'ok':
            self.session.set('tudo_cookie', username)
            next_url = self.get_argument('next_url', '/')
            self.redirect(next_url)
        else:
            return self.redirect('/login?msg={}'.format(ret['msg']))


class LogoutHandler(BaseHandler):
    def get(self):
        self.session.delete('tudo_cookie')
        self.redirect('/')




