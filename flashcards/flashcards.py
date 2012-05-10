"""class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    username = Column(String)
    password = Column(String)
    decks = relationship('Deck')


class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    name = Column(String)
    flashcards = relationship("Flashcard")  # List
    user_id = Column(Integer, ForeignKey('user.id'))  # If no relationship - null


class Flashcard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    question = Column(String)
    answers = Column(PickleType)
    deck_id = Column(Integer, ForeignKey('deck.id'))"""

import logging
logger = logging.getLogger(__name__)

from models import session, User, Deck, Flashcard
from models import lvl1, lvl2, lvl3, lvl4, lvl5
from models import user, deck, flashcard

def promote(flashcard):
    if flashcard.level < 6:
        flashcard.level += 1
        logger.debug("Promoted %s to level %d." % (flashcard, flashcard.level))

    session.commit()

def demote(flashcard):
    pass

def _status(flashcard):
    print "%s is at level %d" % (flashcard, flashcard.level)

_status(flashcard)
promote(flashcard)
_status(flashcard)
