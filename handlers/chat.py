import uuid
import tornado.web
import tornado.escape
from tornado.websocket import WebSocketHandler
from .main import BaseHandler


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render('room.html')


class ChatWSHandler(WebSocketHandler):
    """处理和响应websocket连接"""
    waiters = set()
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
        uid = uuid.uuid4().hex
        chat = {
            'id': uid,
            'html': '<h2 id="m{}">{}</h2>'.format(uid, parsed['body'])
        }
        for w in ChatWSHandler.waiters:
            w.write_message(chat)

    def on_close(self):
        # 客户端关闭连接时，自动调用
        print('close ws connection')
        ChatWSHandler.waiters.remove(self)