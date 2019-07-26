from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from models.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return '<User: {}-{}>'.format(self.id, self.name)

if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all()
