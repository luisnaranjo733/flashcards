"Callable functions to be used by the ui"

import getpass
from database import models

def get_credentials():
    default_username = getpass.getuser() #OS Username
    username = getpass.getpass("Username (ENTER to use %s): " % default_username)
    
    if username.lower() == 'y' or username == '': username = default_username
    
    
    credential = {'username':username,'password':getpass.getpass()}
    return credential

def add_user():
    credential = get_credentials()
    user = models.User(credential['username'],credential['password'])
    models.session.add(user)
    models.session.commit()

add_user()
