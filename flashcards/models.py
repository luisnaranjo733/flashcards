"""sqlalchemy models"""

import os
from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DEBUG = True

import logging
if DEBUG: logtype = logging.DEBUG
if not DEBUG: logtype = logging.INFO

logging.basicConfig(level=logtype)
logger = logging.getLogger(__name__)




PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'database.db')  # Path to DB

engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class DeckError(Exception):
    """For catching errors that have to do with Deck objects."""
    def __init__(self, error=None):
        self.error = error

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    username = Column(String)
    password = Column(String)
    decks = relationship('Deck')

    def __init__(self):
        from datetime import datetime
        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime

    def __repr__(self):
        display_password = '*' * len(self.password)
        return "<User('%s', '%s','%s')>" % (self.username, display_password, self.date_created)

    def add_deck(self, name, repeat=False, ignore_repeat=False):  # Named args untested
        """Create a deck of flashcards on an instance.

Args:

repeat: if true, a deck will be added even if it already exists, without consent.
ignore_repeat: If true, and the deck already exists, the function will just return None.

Returns the deck object if it was created."""
        existing_deck = session.query(Deck).filter_by(name=name).first()

        # If a deck with the title 'name' already exists.
        if existing_deck in self.decks and not repeat and not ignore_repeat:  # TODO: Document repeat and ignore_repeat
            logger.warning("A deck with the title '%s' already exists." % name)
            stop = raw_input("Continue? (y/n)").lower()
            if stop != 'y':
                logger.info("Cancelled the order to add the '%s' deck, because it already existed." % name)
                return

        if existing_deck and ignore_repeat:  # TODO: Document ignore_repeat and what this block of code does.
            return

        deck = Deck()
        deck.name = name
        logger.info("Created a Deck('%s')" % name)

        session.add(deck)
        logger.info("Added the Deck('%s') to the session" % name)

        self.decks.append(deck)
        logger.info("Added the Deck('%s') to the instance list of decks." % name)

        session.commit()
        logger.info("Session commit")

        return deck


    def delete_deck(self, deck_):
        """Removes a deck from self.decks, and *does* delete the deck from the database.

Can take a persisted Deck instance, or the self.name string of Deck instance.

Raises a DeckError if deck_ argument is invalid."""

        DeckInstance = isinstance(deck_, Deck)
        logger.debug("Is %s an instance of Deck? %r" % (deck_, DeckInstance))

        if DeckInstance:

            deck = deck_

        if not DeckInstance:  # Deck var must be a Deck.name of a Deck instance
            try:
                deck = session.query(Deck).filter_by(name=deck_).first()  # Get a deck object using the given name.
                if not deck:
                    raise DeckError

            except DeckError:
                logger.warning("'%s' is NOT a Deck instance OR a Deck instances' Deck.name attribute!" % deck_)
                logger.warning("Deck.delete_deck('%s') failed!" % deck_)
                return

        try:
            self.decks.remove(deck)
            logger.info("Deleted the Deck('%s') from User('%s')" % (deck.name, self.username))

        except ValueError:
            logger.error("ValueError: Deck('%s') does not exist." % deck.name)

        session.delete(deck)
        logger.info("Deleted the Deck('%s') from the database registry" % deck.name)

        session.commit()
        logger.info("Session commit")
            

class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    name = Column(String)
    flashcards = relationship("Flashcard")  # List
    user_id = Column(Integer, ForeignKey('user.id'))  # If no relationship - null

    def __repr__(self):
        return "<Deck of '%s' flashcards>" % self.name

    def __init__(self):
        from datetime import datetime
        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime


class Flashcard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    question = Column(String)
    answers = Column(PickleType)
    correct = Column(Integer)
    incorrect = Column(Integer)
    deck_id = Column(Integer, ForeignKey('deck.id'))

    def __repr__(self):
        return "<Flashcard('%s')>" % self.question[:40]  # First 40 chars

    def __init__(self):
        from datetime import datetime
        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime
        self.correct = 0
        self.incorrect = 0
        self.answers = []

class CardBox(Base):
    __tablename__ = 'cardbox'
    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    flashcards = Column(PickleType)

    def __repr__(self):
        return "<CardBox level('%d')>" % self.level

    def __init__(self):
        self.flashcards = []


Base.metadata.create_all(engine)  # init table?

#Below here are initialized sample objects - for testing.
#========================================================================

user = session.query(User).first()
deck = session.query(Deck).first()
flashcard = session.query(Flashcard).first()
cardbox = session.query(CardBox).first()

if not user and DEBUG:
    user = User()
    user.username = 'luis'
    user.password = 'password'
    logging.info("Created user")
    session.add(user)

if not deck and DEBUG:
    deck = Deck()
    deck.name = 'history'
    logging.info("Created deck")
    session.add(deck)

if not flashcard and DEBUG:
    flashcard = Flashcard()
    flashcard.question = 'When did World War II end?'
    flashcard.answers.append('^1944$')
    logging.info("Created flashcard")
    deck.flashcards.append(flashcard)
    user.decks.append(deck)
    session.add(flashcard)

if not cardbox and DEBUG:
    for level in range(1,6):
        cardbox = CardBox()
        cardbox.level = level
        cardbox.flashcards.append(flashcard)
        logging.info("Created cardbox level %d" % level)
        session.add(cardbox)

session.commit()

#CardBox level containers
#========================================================================

lvl1 = session.query(CardBox).filter_by(level=1).first()
lvl2 = session.query(CardBox).filter_by(level=2).first()
lvl3 = session.query(CardBox).filter_by(level=3).first()
lvl4 = session.query(CardBox).filter_by(level=4).first()
lvl5 = session.query(CardBox).filter_by(level=5).first()
