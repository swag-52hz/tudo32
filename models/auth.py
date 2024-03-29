from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists, and_
from models.db import Base, Session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    email = Column(String(50))
    create_time = Column(DateTime, default=datetime.now())
    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return '<User: {}-{}>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls, username, password):
        session = Session()
        ret = session.query(exists().where(and_(User.name==username,
                                          User.password==password))).scalar()
        session.close()
        return ret


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    # backref:使user对象有posts这个属性访问posts表
    user = relationship('User', back_populates='posts', cascade='all')

    def __repr__(self):
        return '<Post: {}>'.format(self.id)


class LikePost(Base):
    """记录用户标记的喜欢的图片"""
    __tablename__ = 'like_posts'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True, nullable=False)

if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all()
