from models import *
from nose.tools import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

username = 'luis'
password = 'pass'

#========================================================================


user = session.query(User).first()

if not user: # Initialize user if not exist
    user = User()
    user.username = username
    user.password = password
    session.add(user)

total_users = session.query(User).all()

#========================================================================
def init_decks(): #Creates a bunch of decks
    for deck_name in 'spanish math chemistry'.split():
        deck = session.query(Deck).filter_by(name=deck_name).first()
        if not deck: user.add_deck(deck_name, ignore_repeat=True)
init_decks()

print "%s's decks: " % user.username + str(user.decks)

session.commit()
