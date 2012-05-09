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
def init_bundles(): #Creates a bunch of bundles
    for bundle_name in 'spanish math chemistry'.split():
        bundle = session.query(Bundle).filter_by(name=bundle_name).first()
        if not bundle: user.add_bundle(bundle_name, ignore_repeat=True)
init_bundles()

print "%s's bundles: " % user.username + str(user.bundles)

session.commit()
