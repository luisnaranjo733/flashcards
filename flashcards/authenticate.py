"""Authentication for log-in purposes"""

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
    default_username = getpass.getuser()  # OS Username
    statement = "Username (ENTER to use %s): " % default_username
    username = raw_input(statement)

    if username.lower() == 'y' or username == '':
        username = default_username

    password = getpass.getpass()
    date = datetime.now()
    credential = {'username': username, 'password': password}
    print ''
    return credential


def add_user():
    """Adds a user to the database - returns the user object (or None).

    If the username already exists in the database, it will
    hesitate and ask for verification.

    Will return None if the user decides not to create
    a new User because the chosen username already exists."""

     #Retrieve user input as a dictionary - 'username' and 'password' keys
    credential = get_credentials()

    #find all presisted users in the db with the same given username
    existing = session.query(User).filter_by(username=credential['username']).all()

    if existing:
        logger.warning("%s entry already exists!" % credential['username'])
        verification = raw_input("Add anyway? (Y/N):\t").upper()
        statement = "Adding duplicate username '%s'" % credential['username']
        if verification == 'Y':
            existing = False
            logger.debug(statement)

    if not existing:
        print("Adding'%s' to the database..." % credential['username'])
        user = User()
        user.username = credential['username']
        user.password = credential['password']

        session.add(user)
        session.commit()

        return user


def authenticate():
    """Authenticates an existing user.
    Returns object if successful, or None."""

    credential = get_credentials()
    username = credential['username']
    password = credential['password']
    successful = session.query(User).filter(and_(User.username == username, User.password == password)).scalar()
    time = datetime.now()

    if successful:
        print "You have succesfully authenticated.\n"

        string = "'{user}' successfully authenticated at '{time}'"
        logger.debug(string.format(user=username, time=time))

    if not successful:
        print "Incorrect username or password!\n"
        logger.debug("Someone unsuccessfully tried to authenticate '%s' at '%s'" % (username, time))

    return successful


def show_users():
    """Displays a list of all the authenticated users.
    Usage is safe - __repr__ shows asterisks, not the password.
    Returns the list of users in the database."""

    users = session.query(User).all()

    if not users:
        users = "No users registered in the database!"

    pprint(users)
    logger.debug("Displayed all users")

    return users


def delete_user():
    """Delete a user. That is all."""

    user = authenticate()

    if user:
        session.delete(user)
        session.commit()
        time = strftime('%x %X')
        statement = "Removed %s from database at %s" % (user.username, time)
        print statement
