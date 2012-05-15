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
from models import lvl1, lvl2, lvl3, MAXLEVEL
from models import user, deck, flashcard

def promote(flashcard, response_time=None):
    """For moving the flashcards from box to box (Leitner system).

Moves the given flashcard up by one level, with level 6 at the top"""

    if flashcard.level < MAXLEVEL:
        flashcard.level += 1
        logger.info("Promoted %s to level %d." % (flashcard, flashcard.level))

    flashcard.correct += 1

    if response_time:
        flashcard.history.append((response_time, True))

    session.commit()

    logger.warning("Couldn't promote %s because it's level is already %d." % (flashcard, MAXLEVEL))



def demote(flashcard, response_time=None):
    """For reseting the level of a flashcard (Leitner system)."""

    flashcard.level = 1
    flashcard.incorrect += 1
    if response_time:
        flashcard.history.append((response_time, False))

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
        print card.history

def _review(flashcard):
    time_asked = datetime.now()

    print flashcard.question
    attempt = raw_input("> ")

    response_time = -(time_asked - datetime.now()).total_seconds()

    for pattern in flashcard.answers:
        match = re.match(pattern, attempt)
        logger.debug("Matched '%s' to '%s'" % (pattern, attempt))
        if match:
            promote(flashcard, response_time)

        if not match:
            demote(flashcard, response_time)
        print response_time

def _leitner():
    while current_state().level < 3:
        flashcards = current_state().cards()
        for flashcard in flashcards:
            _review(flashcard)

_info()
