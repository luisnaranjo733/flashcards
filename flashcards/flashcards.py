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

from models import session, User, Deck, Flashcard
import logging
logger = logging.getLogger(__name__)

def leitner(deck):
    """Leitner system based on space repitition for efficient memorization."""

    pass

user = session.query(User).first()
deck = session.query(Deck).first()
flashcard = session.query(Deck).first()

leitner(deck)

