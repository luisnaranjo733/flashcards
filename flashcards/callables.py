"Callable functions to be used by the ui"

import getpass
from datetime import datetime
from models import session, User
from sqlalchemy import and_
from pprint import pprint

def get_credentials():
    default_username = getpass.getuser() #OS Username
    username = getpass.getpass("Username (ENTER to use %s): " % default_username)
    
    if username.lower() == 'y' or username == '': username = default_username
    password = getpass.getpass()
    date = datetime.now()
    
    credential = {'username':username,'password':password}#,'date':date}
    return credential

def add_user():
    credential = get_credentials()
    
    existing = session.query(User).filter_by(username=credential['username']).all()
    if existing:
        print "%s entry already exists!" % credential['username']
        return
    if not existing:
        print "Creating database entry for '%s'" % credential['username']
        user = User(credential['username'],credential['password'])#,credential['date'])
        session.add(user)
        session.commit()

def login():
    credential = get_credentials()
    successful = session.query(User).filter(and_(User.username == credential['username'], User.password == credential['password'])).scalar()
    
    if successful:
        print "Congradulations! You have succesfully logged in!"
        
    if not successful:
        print "Incorrect username or password!\nTry again!"

def show_users(): #potentially dangerous!
    users = session.query(User).all()
    information = []
    
    for user in users:
        block = (str(user.username),str(user.date))
        information.append(block)
        
    pprint(information)

