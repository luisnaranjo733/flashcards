"Test script - not important"

import logging
logger = logging.getLogger(__name__)

from models import *

user = session.query(User).first()
bundle = session.query(Bundle).first()
flashcard = session.query(Bundle).first()

if not user or not bundle or not flashcard:
    user = User()
    user.username = 'luis'
    user.password = 'password'
    session.add(user)
    logging.info("Created user")

    bundle = Bundle()
    bundle.name = 'history'
    session.add(bundle)
    logging.info("Created bundle")


    flashcard = Flashcard()
    flashcard.question = 'When did World War II end?'
    flashcard.answers = ['^1944$']
    session.add(flashcard)
    logging.info("Created flashcard")

    bundle.flashcards.append(flashcard)
    user.bundles.append(bundle)

    session.commit()



print user
print user.bundles[0]
print user.bundles[0].flashcards[0].question
print user.bundles[0].flashcards[0].answers
print user.bundles[0].flashcards[0].correct
print user.bundles[0].flashcards[0].incorrect


