"Test script - not important"

import logging
logger = logging.getLogger(__name__)

from models import *




print user
print user.decks[0]
print user.decks[0].flashcards[0].question
print user.decks[0].flashcards[0].answers
print user.decks[0].flashcards[0].correct
print user.decks[0].flashcards[0].incorrect
print cardbox


