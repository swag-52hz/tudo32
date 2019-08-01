import uuid
import os
from PIL import Image


class UploadImage(object):
    thumb_size = (200, 200)

    def __init__(self, ext_name, static_path):
        self.ext_name = ext_name
        self.static_path = static_path
        self.upload_dir = 'uploads'
        self.thumb_dir = 'thumbs'
        self.new_name = self.get_new_name

    @property
    def get_new_name(self):
        return uuid.uuid4().hex + self.ext_name

    @property
    def get_image_path(self):
        return os.path.join(self.upload_dir, self.new_name)

    @property
    def save_to(self):
        return os.path.join(self.static_path, self.get_image_path)

    def save_content(self, body):
        with open(self.save_to, 'wb') as f:
            f.write(body)

    @property
    def get_thumb_url(self):
        name, ext_name = os.path.splitext(self.new_name)
        thumb_name = '{}_{}*{}{}'.format(name,
                                         self.thumb_size[0],
                                         self.thumb_size[1],
                                         ext_name)
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    def save_thumb_img(self):
        img = Image.open(self.save_to)
        img.thumbnail(self.thumb_size)
        img.save(os.path.join(self.static_path, self.get_thumb_url))




