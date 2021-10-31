from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import database_uri


Base = declarative_base()
engine = create_engine(database_uri)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User('{self.name}', ID:'{self.id}')>"


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    user = Column(Integer, ForeignKey('user.id'))

    def __init__(self, message, user_id):
        self.message = message
        self.user = user_id

    def __repr__(self):
        return f"<Message(ID:'{self.id}', from user ID:'{self.user}')>"
