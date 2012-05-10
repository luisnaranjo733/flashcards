from models import session, DEBUG, User, Deck, Flashcard, CardBox
import logging

if DEBUG: loglevel = logging.DEBUG
if not DEBUG: loglevel = logging.INFO

logger = logging.getLogger(__name__)
logging.basicConfig(level=loglevel)  # DEBUG is a var from models!

from models import lvl1, lvl2, lvl3, MAXLEVEL
from models import user, deck, flashcard

def promote(flashcard):
    """For moving the flashcards from box to box (Leitner system).

Moves the given flashcard up by one level, with level 6 at the top"""

    if flashcard.level < MAXLEVEL:
        flashcard.level += 1
        logger.info("Promoted %s to level %d." % (flashcard, flashcard.level))
        session.commit()
        return True

    logger.debug("Couldn't promote %s because it's level is already %d." % (flashcard, MAXLEVEL))
    return False


def demote(flashcard):
    """For reseting the level of a flashcard (Leitner system)."""

    flashcard.level = 1
    session.commit()
    logger.info("Demoted %s to level %d." % (flashcard, flashcard.level))


def current_state():
    """Returns a cardbox instance, judging by the lowest level card.

We don't progress a level until there are no flashcards on that level.
When we reach the final level, we are done."""

    levels = [flashcard.level for flashcard in session.query(Flashcard).all()]
    levels.sort()
    lowest = levels[0]
    return session.query(CardBox).filter_by(level=lowest).first()

def _info(): #Display info for debugging
    for card in session.query(Flashcard).all():
        print card
        print card.level


print lvl1.cards()
print lvl2.cards()

