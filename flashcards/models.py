"""sqlalchemy models"""

from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import os

DEBUG = False

if not DEBUG:
    PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'database.db') #Path to DB
if DEBUG:
    PATH = ':memory:'
    
engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

        
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    username = Column(String)
    password = Column(String)
    sets = relationship('Set')
   
    def __init__(self):
        from datetime import datetime
        
        self.date_created = datetime.now() #datetime.datetime object - converted back and forth from string
        del datetime
                    
    def __repr__(self):
        display_password = '*' * len(self.password)
        return "<User('%s', '%s','%s')>" % (self.username, display_password, self.date_created)

class Set(Base):
    __tablename__ = 'set'
    
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    name = Column(String)
    
    flashcards = relationship("Flashcard")
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return "<Set of '%s' flashcards>" % self.name
    
    def __init__(self):
        from datetime import datetime
        
        self.date_created = datetime.now() #datetime.datetime object - converted back and forth from string
        del datetime
        
class Flashcard(Base):
    __tablename__ = 'flashcard'
    
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    question = Column(String)
    answers = Column(PickleType)
    
    set_id = Column(Integer, ForeignKey('set.id'))

    def __repr__(self):
        return "<Flashcard(%s)>" % self.question[:20] #First 20 chars

    def __init__(self):
        from datetime import datetime
        
        self.date_created = datetime.now() #datetime.datetime object - converted back and forth from string
        del datetime
        

Base.metadata.create_all(engine) #init table?


