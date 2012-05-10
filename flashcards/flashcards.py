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

from models import session, DEBUG, User, Deck, Flashcard
import logging

if DEBUG: loglevel = logging.DEBUG
if not DEBUG: loglevel = logging.INFO

logger = logging.getLogger(__name__)
logging.basicConfig(level=loglevel)  # DEBUG is a var from models!

from models import lvl1, lvl2, lvl3, lvl4, lvl5, MAXLEVEL
from models import user, deck, flashcard

def promote(flashcard):
    """For moving the flashcards from box to box (Leitner system).

Moves the given flashcard up by one level, with level 6 at the top"""

    if flashcard.level < MAXLEVEL:
        flashcard.level += 1
        logger.info("Promoted %s to level %d." % (flashcard, flashcard.level))
        session.commit()
        return

    logger.debug("Couldn't promote %s because it's level is already %d." % (flashcard, MAXLEVEL))


def demote(flashcard):
    """For reseting the level of a flashcard (Leitner system)."""

    flashcard.level = 1
    session.commit()
    logger.info("Demoted %s to level %d." % (flashcard, flashcard.level))
