"""sqlalchemy models"""

import os
from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

MAXLEVEL = 3

import logging
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel)
logger = logging.getLogger(__name__)

PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'database.db')  # Path to DB

engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    decks = relationship('Deck')

    def __repr__(self):
        display_password = '*' * len(self.password)
        return "<User('%s', '%s','%s')>" % (self.username, display_password, self.date_created)


class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    flashcards = relationship("Flashcard")  # List
    user_id = Column(Integer, ForeignKey('user.id'))  # If no relationship - null

    def __repr__(self):
        return "<Deck of '%s' flashcards>" % self.name


class Flashcard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answers = Column(PickleType)  # TODO: Is this ok?
    correct = Column(Integer)
    incorrect = Column(Integer)
    level = Column(Integer)
    deck_id = Column(Integer, ForeignKey('deck.id'))  # Who I belong to

    def __repr__(self):
        return "<Flashcard('%s')>" % self.question[:40]  # First 40 chars

    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.level = 1  # Start at level 1
        self.answers = []


class CardBox(Base):
    __tablename__ = 'cardbox'
    id = Column(Integer, primary_key=True)
    level = Column(Integer)

    def __repr__(self):
        return "<CardBox level('%d')>" % self.level

    def cards(self):
        return session.query(Flashcard).filter_by(level=self.level).all()


Base.metadata.create_all(engine)  # init table

levels = session.query(CardBox).all()

if len(levels) == 0 or len(levels) < MAXLEVEL:  # Init leitner cardboxes
    for level in range(1, 1+MAXLEVEL):
        cardbox = CardBox()
        cardbox.level = level
        logger.info("Created cardbox level %d" % level)
        session.add(cardbox)
        levels.append(cardbox)

session.commit()  # TODO: Is this a performance issue?
