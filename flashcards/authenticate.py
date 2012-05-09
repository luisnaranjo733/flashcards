"Callable functions to be used by the ui"

import getpass
from datetime import datetime
from models import session, User
from sqlalchemy import and_
from pprint import pprint

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------
# Login stuff

def get_credentials():
    default_username = getpass.getuser() #OS Username
    username = getpass.getpass("Username (ENTER to use %s): " % default_username)
    
    if username.lower() == 'y' or username == '': username = default_username
    password = getpass.getpass()
    date = datetime.now()
    
    credential = {'username':username,'password':password}
    print ''
    return credential

def add_user():
    """Adds a user to the database - returns the user object.
    
    If the username already exists in the database, it will
    hesitate and ask for verification."""
    
    credential = get_credentials() #Retrieve user input as a dictionary - 'username' and 'password' keys
    
    existing = session.query(User).filter_by(username=credential['username']).all() #find all presisted users in the db with the same given username
    
    if existing:
        logger.warning("%s entry already exists!" % credential['username'])
        verification = raw_input("Add anyway? (Y/N):\t").upper()
        if verification == 'Y':
            existing = False
            logger.debug("Adding duplicate username '%s'" % credential['username'])

    if not existing:
        logger.info("Creating database entry for '%s'" % credential['username'])
        user = User()
        user.username = credential['username']
        user.password = credential['password']
        
        session.add(user)
        session.commit()
    
    return user

def login():
    """Authenticates an existing user."""
    
    credential = get_credentials()
    successful = session.query(User).filter(and_(User.username == credential['username'], User.password == credential['password'])).scalar()
    
    if successful:
        print "Congradulations! You have succesfully logged in!"
        
    if not successful:
        print "Incorrect username or password!\nTry again!"

def show_users(): # Safe - __repr__ shows asterisks not password
    """Displays a list of all the authenticated users."""
    
    users = session.query(User).all()
    
    if not users: users = "No users in the database yet!"
    
    pprint(users)

#------------------------------------------------------------------------
# Flashcard db stuff

