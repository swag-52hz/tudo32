from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOST_NAME = '127.0.0.1'
PORT = '3306'
DB_NAME = 'tudo32'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOST_NAME, PORT, DB_NAME
)
engine = create_engine(DB_URL)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())
