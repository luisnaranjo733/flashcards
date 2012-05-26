from models import *
import logging

user = session.query(User).first()
deck = session.query(Deck).first()
flashcard = session.query(Flashcard).first()

if not user:
    user = User()
    user.username = 'luis'
    user.password = 'password'
    logging.info("Created user")
    session.add(user)

if not deck:
    deck = Deck()
    deck.name = 'history'
    logging.info("Created deck")
    session.add(deck)

if not flashcard:
    flashcard1 = Flashcard()
    flashcard1.question = 'When did World War II end?'  # Add a question to this flashcard
    flashcard1.answers.append('^1944$') #Add a answer to this flashard
    logging.info("Created flashcard (level 1)")
    deck.flashcards.append(flashcard1)  # Add this flashcard to the deck instance created above
    session.add(flashcard1)  # Add to the sqlalchemy session

    flashcard2 = Flashcard()
    flashcard2.question = "When is Luis' birthday?"
    flashcard2.answers.append('^1995$')
    flashcard2.level = 2  # Defaults to 1 on __init__
    logging.info("Created flashcard (level 2)")
    deck.flashcards.append(flashcard2)
    session.add(flashcard2)

    flashcard3 = Flashcard()
    flashcard3.question = "What school does Luis go to?"
    flashcard3.answers.append('^[Bb]ishop +[Bb]lanchet *([Hh]igh +?)?([Ss]chool)?$')
    flashcard3.level = 3  # Defaults to 1 on __init__
    logging.info("Created flashcard (level 3)")
    deck.flashcards.append(flashcard3)
    session.add(flashcard3)

    user.decks.append(deck)  # Add the deck with flashcards in it to the user's list of decks.

session.commit()
