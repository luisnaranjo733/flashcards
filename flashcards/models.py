"""sqlalchemy models"""

import os
from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DEBUG = True
MAXLEVEL = 3

import logging
if DEBUG: loglevel = logging.DEBUG
if not DEBUG: loglevel = logging.INFO

logging.basicConfig(level=loglevel)
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
    history = Column(PickleType)
    question = Column(String)
    answers = Column(PickleType)
    correct = Column(Integer)
    incorrect = Column(Integer)
    level = Column(Integer)
    deck_id = Column(Integer, ForeignKey('deck.id'))  # Who I belong to

    def __repr__(self):
        return "<Flashcard('%s')>" % self.question[:40]  # First 40 chars

    def __init__(self):
        from datetime import datetime
        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime
        self.correct = 0
        self.incorrect = 0
        self.level = 1  # Start at level 1
        self.answers = []
        self.history = []  #TODO: Implement this Tuple(date accessed, time spent thinking, right/wrong)

        
class CardBox(Base):
    __tablename__ = 'cardbox'
    id = Column(Integer, primary_key=True)
    level = Column(Integer)

    def __repr__(self):
        return "<CardBox level('%d')>" % self.level

    def cards(self):
        return session.query(Flashcard).filter_by(level=self.level).all()


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
    flashcard1 = Flashcard()
    flashcard1.question = 'When did World War II end?'  # Add a question to this flashcard
    flashcard1.answers.append('^1944$') #Add a answer to this flashard
    logging.info("Created flashcard (level 1)")
    deck.flashcards.append(flashcard1)  # Add this flashcard to the deck instance created above
    session.add(flashcard1)  # Add to the sqlalchemy session

    flashcard2 = Flashcard()
    flashcard2.question = "When is Luis' birthday?"
    flashcard2.answers.append('^1995$')
    flashcard2.level = 2  # Defaults to 1 on __init__
    logging.info("Created flashcard (level 2)")
    deck.flashcards.append(flashcard2)
    session.add(flashcard2)

    flashcard3 = Flashcard()
    flashcard3.question = "What school does Luis go to?"
    flashcard3.answers.append('^[Bb]ishop +[Bb]lanchet *([Hh]igh +?)?([Ss]chool)?$')
    flashcard3.level = 3  # Defaults to 1 on __init__
    logging.info("Created flashcard (level 3)")
    deck.flashcards.append(flashcard3)
    session.add(flashcard3)

    user.decks.append(deck)  # Add the deck with flashcards in it to the user's list of decks.

if not cardbox and DEBUG:
    for level in range(1, MAXLEVEL+1):
        cardbox = CardBox()
        cardbox.level = level
        logging.info("Created cardbox level %d" % level)
        session.add(cardbox)

session.commit()

#CardBox level containers
#========================================================================

lvl1 = session.query(CardBox).filter_by(level=1).first()
lvl2 = session.query(CardBox).filter_by(level=2).first()
lvl3 = session.query(CardBox).filter_by(level=3).first()
