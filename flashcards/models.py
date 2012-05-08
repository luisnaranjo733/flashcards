from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pprint import pprint
import os

DEBUG = False
PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__))
        ,os.path.join('data','flashcards.db')) #Path to DB

engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=DEBUG)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    date = Column(DateTime)
   
    def __init__(self, username, password, date):
        self.username = username
        self.password = password
        self.date = date #datetime.datetime object - converted back and forth from string
   
    def __repr__(self):
       return "<User('%s', '%s','%s')>" % (self.username, self.password, self.date)
 
      
Base.metadata.create_all(engine) #init table?

def show_users(): #potentially dangerous!
    users = session.query(User).all()
    user_names = [user.username for user in users]
    pprint(user_names)

session.commit()

if __name__ == '__main__':
    show_users()
