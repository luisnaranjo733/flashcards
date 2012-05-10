"""class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    username = Column(String)
    password = Column(String)
    bundles = relationship('Bundle')


class Bundle(Base):
    __tablename__ = 'bundle'
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
    bundle_id = Column(Integer, ForeignKey('bundle.id'))"""

from models import session, User, Bundle, Flashcard
import logging
logger = logging.getLogger(__name__)

def leitner(bundle):
    """Leitner system based on space repitition for efficient memorization."""

    logger.info("Initializing leitner system on %s" % bundle)
    for flashcard in bundle.flashcards:
        if flashcard.correct == None:
            flashcard.correct = 0
            logger.info("Initialized the tally of correct answers on %s" % flashcard)
        if flashcard.incorrect == None:
            flashcard.incorrect = 0
            logger.info("Initialized the tally of incorrect answers on %s" % flashcard)

        session.commit()

user = session.query(User).first()
bundle = session.query(Bundle).first()
flashcard = session.query(Bundle).first()

leitner(bundle)

