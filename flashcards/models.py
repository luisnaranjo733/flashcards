from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import os

DEBUG = False

if not DEBUG:
    PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__))
            ,os.path.join('data','flashcards.db')) #Path to DB
if DEBUG:
    PATH = ':memory:'
    
engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

        
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    username = Column(String)
    password = Column(String)
    #TODO: relationship('sets')
   
    def __init__(self):
        from datetime import datetime
        
        date = datetime.now()
        self.date = date #datetime.datetime object - converted back and forth from string
        del datetime
                    
    def __repr__(self):
       return "<User('%s', '%s','%s')>" % (self.username, self.password, self.date)

class Set(Base):
    __tablename__ = 'set'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String)
    
    flashcards = relationship("Flashcard")

    def __repr__(self):
        return "<Set of '%s' flashcards>" % self.name
    
    def __init__(self):
        from datetime import datetime
        
        date = datetime.now()
        self.date = date #datetime.datetime object - converted back and forth from string
        del datetime
        
class Flashcard(Base):
    __tablename__ = 'flashcard'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    question = Column(String)
    answers = Column(PickleType)
    
    parent_id = Column(Integer, ForeignKey('set.id'))

    def __repr__(self):
        return "<Flashcard(%s)>" % self.question[:20] #First 20 chars

    def __init__(self):
        from datetime import datetime
        
        date = datetime.now()
        self.date = date #datetime.datetime object - converted back and forth from string
        del datetime
        

Base.metadata.create_all(engine) #init table?


