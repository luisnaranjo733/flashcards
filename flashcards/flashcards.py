"""This script will implement the leitner algorithm for sorting flashcards.

It includes 3 pre-build instances of CardBox (levels 1-3)
"""

from models import session, DEBUG, User, Deck, Flashcard, CardBox
import logging
import re
from datetime import datetime

if DEBUG: loglevel = logging.DEBUG
if not DEBUG: loglevel = logging.INFO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)  # DEBUG is a var from models!

logger = logging
from models import levels, MAXLEVEL

def promote(flashcard):
    """For moving the flashcards from box to box (Leitner system).

Moves the given flashcard up by one level, with level 3 at the top."""

    flashcard.correct += 1

    if flashcard.level < MAXLEVEL:
        flashcard.level += 1
        logger.info("Promoted %s to level %d." % (flashcard, flashcard.level))

    session.commit()


def demote(flashcard):
    """For reseting the level of a flashcard (Leitner system)."""

    if flashcard.level > 1:
        flashcard.level = 1
        flashcard.incorrect += 1
        logger.info("Demoted %s to level %d." % (flashcard, flashcard.level))

    session.commit()



def current_state():
    """Returns a cardbox instance, judging by the lowest level card.

We don't progress a level until there are no flashcards on that level.
When we reach the final level, we are done."""

    flashcard_levels = [flashcard.level for flashcard in session.query(Flashcard).all()]
    flashcard_levels.sort()
    if flashcard_levels:
        lowest = flashcard_levels[0]
    if not flashcard_levels:
        raise Exception("No flashcards in the system yet!")

    return session.query(CardBox).filter_by(level=lowest).first()



# Private helper functions for development
#========================================================================


def _promote_all():
    for card in session.query(Flashcard).all():
        promote(card)


def _demote_all():
    for card in session.query(Flashcard).all():
        demote(card)


def _info(): #Display info for debugging
    for card in session.query(Flashcard).all():
        print("%s is at level %d." % (card,card.level))
