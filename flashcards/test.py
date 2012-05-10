"Test script - not important"

import logging
logger = logging.getLogger(__name__)

from models import *

user = session.query(User).first()
deck = session.query(Deck).first()
flashcard = session.query(Deck).first()

if not user or not deck or not flashcard:
    user = User()
    user.username = 'luis'
    user.password = 'password'
    session.add(user)
    logging.info("Created user")

    deck = Deck()
    deck.name = 'history'
    session.add(deck)
    logging.info("Created deck")


    flashcard = Flashcard()
    flashcard.question = 'When did World War II end?'
    flashcard.answers = ['^1944$']
    session.add(flashcard)
    logging.info("Created flashcard")

    deck.flashcards.append(flashcard)
    user.decks.append(deck)

    session.commit()



print user
print user.decks[0]
print user.decks[0].flashcards[0].question
print user.decks[0].flashcards[0].answers
print user.decks[0].flashcards[0].correct
print user.decks[0].flashcards[0].incorrect


