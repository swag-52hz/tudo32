import logging
import requests
import tornado.web
from tornado.gen import coroutine, sleep
from tornado.httpclient import AsyncHTTPClient
from .main import BaseHandler
from .chat import ChatWSHandler, make_data
from utils.photo import UploadImage


logger = logging.getLogger('super.log')


class SyncHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        resp = requests.get(save_url)
        upload_img = UploadImage('.jpg', self.application.settings['static_path'])
        upload_img.save_content(resp.content)
        upload_img.save_thumb_img()
        post_id = self.orm.add_post(self.current_user, upload_img.get_image_path, upload_img.get_thumb_url)
        if post_id:
            self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('upload error')


class AsyncHandler(BaseHandler):
    """使用协程以及异步并发,save API 保存指定url图片"""
    @coroutine
    def get(self):
        username = self.get_argument('name', '')
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        content = yield self.get_image(save_url)
        if content:
            upload_img = UploadImage('.jpg', self.application.settings['static_path'])
            upload_img.save_content(content)
            upload_img.save_thumb_img()
            post_id = self.orm.add_post(username, upload_img.get_image_path, upload_img.get_thumb_url)
            if post_id:
                chat = make_data(self, '{} save to http://127.0.0.1:8000/post/{} by {}'.format(save_url, post_id, username), 'admin')
                ChatWSHandler.update_history(chat['html'])
                ChatWSHandler.send_message(chat)
            else:
                logger.warning('%s save to post error', save_url)
        else:
            logger.warning("%s fetch error"% save_url)
            self.write("url fetch error")

    @coroutine
    def get_image(self, url):
        http_client = AsyncHTTPClient()
        resp = yield http_client.fetch(url, request_timeout=45)
        # yield sleep(15)
        logger.info(resp.code)
        if resp.code is 200:
            return resp.body
        else:
            return None
