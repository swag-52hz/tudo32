import uuid
import logging
import tornado.web
import tornado.escape
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.httpclient import AsyncHTTPClient
from datetime import datetime
from .main import BaseHandler

logger = logging.getLogger('tudo.log')


def make_data(handler, body, username):
    chat = {
        'id': uuid.uuid4().hex,
        'body': body,
        'username': username,
        'created': datetime.now().strftime('%Y年%m月%d日 %H:%M'),
    }
    chat['html'] = tornado.escape.to_basestring(handler.render_string('message.html', chat=chat))
    return chat


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render('room.html', history=ChatWSHandler.history)


class ChatWSHandler(WebSocketHandler, BaseHandler):
    """处理和响应websocket连接"""
    waiters = set()
    history = []
    history_size = 20

    def open(self):
        # 新的websocket连接打开，自动调用
        print('new wb connection')
        ChatWSHandler.waiters.add(self)

    def on_message(self, message):
        # websocket服务端收到消息自动调用
        print('got message: {}'.format(message))
        # 服务端给客户端发消息
        # self.write_message('got: [{}]'.format(message))
        parsed = tornado.escape.json_decode(message)
        body = parsed['body']
        if body.startswith('http://') or body.startswith('https://'):
            save_url = body
            api_url = 'http://127.0.0.1:8000/save?name={}&save_url={}'.format(self.current_user, save_url)
            logger.info(api_url)
            client = AsyncHTTPClient()
            IOLoop.current().spawn_callback(client.fetch, api_url, request_timeout=45)
            chat = make_data(self, 'url is processing {}'.format(save_url), 'admin')
            self.write_message(chat)
        else:
            chat = make_data(self, parsed['body'], self.current_user)
            ChatWSHandler.update_history(chat['html'])
            ChatWSHandler.send_message(chat)

    @classmethod
    def update_history(cls, chat):
        # 保存最后20条信息
        cls.history.append(chat)
        if len(cls.history) > cls.history_size:
            cls.history = cls.history[-cls.history_size:]

    @classmethod
    def send_message(cls, chat):
        # 发送消息
        for w in cls.waiters:
            w.write_message(chat)

    def on_close(self):
        # 客户端关闭连接时，自动调用
        print('close ws connection')
        ChatWSHandler.waiters.remove(self)

    def get_compression_options(self):
        # 返回一个空字典可以打开压缩
        return {}