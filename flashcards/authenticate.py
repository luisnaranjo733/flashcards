"""Authentication for log-in purposes"""

import getpass
from datetime import datetime
from time import strftime
from models import session, User
from sqlalchemy import and_
from pprint import pprint

import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------
# Login stuff


class AuthenticationError(Exception):
    """A general authentication error."""

    def __init__(self, message=''):
        Exception.__init__(self)
        self.message = message


def get_credentials():
    """Helper function for getting user input.

    Retuns a dict with 'username' and 'password' keys."""
    default_username = getpass.getuser()  # OS Username
    statement = "Username (ENTER to use %s): " % default_username
    username = raw_input(statement)

    if username.lower() == 'y' or username == '':
        username = default_username

    password = getpass.getpass()
    date = datetime.now()
    print ''
    return (username, password)


def add_user(username=None, password=None):
    """Adds a user to the database - returns the user object (or None).

    If the username already exists in the database, it will
    hesitate and ask for verification.

    If only username or only password is passed:
    will raise AuthenticationError

    Will return None if the user decides not to create
    a new User because the chosen username already exists."""

     #Retrieve user input as a dictionary - 'username' and 'password' keys
    if not username and not password:
        username, password = get_credentials()

    # If only one credential is passed

    try:
        if (not username and password) or ((not password and password != '') and username):
            raise AuthenticationError("Need both username and password")

    except AuthenticationError, Error:
        print Error.message
        logger.debug(Error.message)

    #find all presisted users in the db with the same given username
    existing = session.query(User).filter_by(username=username).all()

    if existing:
        logger.warning("%s entry already exists!" % username)
        verification = raw_input("Add anyway? (Y/N):\t").upper()
        if verification == 'Y':
            existing = False
            logger.debug("Adding duplicate username '%s'" % username)

    if not existing:
        print("Adding'%s' to the database..." % username)
        user = User()
        user.username = username
        user.password = password

        session.add(user)
        session.commit()

        return user


def authenticate(user=None):
    """Authenticates an existing user.

    If a user is passed as an argument,
    it will try to authenticate it.

    If no user is passed, it asks for user input.
    Returns object if successful, or None."""

    if not user:
        username, password = get_credentials()

    if user:
        username = user.username
        password = user.password

    successful = session.query(User).filter(and_(User.username == username, User.password == password)).scalar()
    time = datetime.now()

    if successful:
        print "You have succesfully authenticated.\n"

        string = "'{user}' successfully authenticated at '{time}'"
        logger.debug(string.format(user=username, time=time))

    if not successful:
        print "Incorrect username or password!\n"
        logger.info("Someone unsuccessfully tried to authenticate '%s' at '%s'" % (username, time))

    logger.debug("Returning from authenticate funtion")
    return successful


def __show_users():  # NOT PUBLIC
    """Displays a list of all the authenticated users.
    Usage is safe - __repr__ shows asterisks, not the password.
    Returns the list of users in the database."""

    users = session.query(User).all()

    if not users:
        users = "No users registered in the database!"

    pprint(users)
    logger.debug("Displayed all users")

    return users


def delete_user(user=None):
    """Delete a user.

If a user *isn't* passed,
the user will be asked to
authenticate his/her username.

If a user *is* passed, the
user will be deleted with
**no verification**, so be
careful."""

    users = "Users: " + ', '.join([str(USER.username) for USER in session.query(User).all()])

    pprint(users)

    logger.info("User var: " + str(user))  # user var is getting an ORM object!???? should be None TODO: Remove this line

    if not user:
        authenticated = authenticate()

    if user:
        authenticated = authenticate(user)  # TODO:None for user is deleting anyways? 

    if authenticated and authenticated.id:  # id is to make sure it is persisted.
        logger.info("User var in if clause: " + str(authenticated))
        session.delete(authenticated)
        session.commit()
        logger.debug("Deleted %s" % authenticated)
        time = strftime('%x %X')
        statement = "Removed %s from database at %s" % (authenticated.username, time)
        print statement

#from authenticate import *
