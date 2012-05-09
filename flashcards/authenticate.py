"Callable functions to be used by the ui"

import getpass
from datetime import datetime
from time import strftime
from models import session, User
from sqlalchemy import and_
from pprint import pprint

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------
# Login stuff

def get_credentials():
    """Helper function for getting user input.
    
    Retuns a dict with 'username' and 'password' keys."""
    
    default_username = getpass.getuser() #OS Username
    username = getpass.getpass("Username (ENTER to use %s): " % default_username)
    
    if username.lower() == 'y' or username == '': username = default_username
    password = getpass.getpass()
    date = datetime.now()
    
    credential = {'username':username,'password':password}
    print ''
    return credential

def add_user():
    """Adds a user to the database - returns the user object (or None).
    
    If the username already exists in the database, it will
    hesitate and ask for verification.
    
    Will return None if the user decides not to create
    a new User because the chosen username already exists."""
    
    credential = get_credentials() #Retrieve user input as a dictionary - 'username' and 'password' keys
    
    existing = session.query(User).filter_by(username=credential['username']).all() #find all presisted users in the db with the same given username
    
    if existing:
        logger.warning("%s entry already exists!" % credential['username'])
        verification = raw_input("Add anyway? (Y/N):\t").upper()
        if verification == 'Y':
            existing = False
            logger.debug("Adding duplicate username '%s'" % credential['username'])

    if not existing:
        logger.debug("Creating database entry for '%s'" % credential['username'])
        user = User()
        user.username = credential['username']
        user.password = credential['password']
        
        session.add(user)
        session.commit()
    
        return user

def login():
    """Authenticates an existing user. Returns object if successful, or None."""
    
    credential = get_credentials()
    successful = session.query(User).filter(and_(User.username == credential['username'], User.password == credential['password'])).scalar()
    
    if successful:
        print "You have succesfully authenticated.\n"
        logger.debug("'{user}' successfully authenticated at '{time}'".format(user=credential['username'],time=datetime.now()))
        
    if not successful:
        print "Incorrect username or password!\n"
        logger.debug("Someone unsuccessfully tried to authenticate into '{user}' at '{time}'".format(user=credential['username'],time=datetime.now()))

    return successful
    
def show_users(): # 
    """Displays a list of all the authenticated users.
    Usage is safe - __repr__ shows asterisks, not the password.
    Returns the list of users in the database."""
    
    users = session.query(User).all()

    if not users: users = "No users registered in the database!"
    
    pprint(users)
    logger.debug("Displayed all users")
    
    return users

def delete_user():
    """Delete a user. That is all."""
    
    user = login()
    
    if user:
        session.delete(user)
        session.commit()
        statement = "Deleted {user} from the database at {time}".format(user=user.username,time=strftime('%x %X'))
        print statement
        
    
    
#------------------------------------------------------------------------
# Flashcard db stuff

