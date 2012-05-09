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

bundle_name = 'history'
bundle = session.query(Bundle).filter_by(name=bundle_name).first()

if not bundle:
    bundle = user.add_bundle(bundle_name,ignore_repeat=True)

print "%s's bundles: " % user.username + str(user.bundles)

user.delete_bundle(bundle_name) #TODO: Works the first time
session.commit()
