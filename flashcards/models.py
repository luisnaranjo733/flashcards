"""sqlalchemy models"""

from sqlalchemy import Column, Integer, String, create_engine, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import os

DEBUG = False

if not DEBUG:
    PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'database.db')  # Path to DB
if DEBUG:
    PATH = ':memory:'

engine = create_engine('sqlite:///{path}'.format(path=PATH), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    username = Column(String)
    password = Column(String)
    bundles = relationship('Bundle')

    def __init__(self):
        from datetime import datetime

        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime

    def __repr__(self):
        display_password = '*' * len(self.password)
        return "<User('%s', '%s','%s')>" % (self.username, display_password, self.date_created)

    def add_bundle(self, name):
        """Create a bundle of flashcards on an instance.

Returns the bundle object if it was created."""

        existing = session.query(Bundle).filter_by(name=name).first()

        if existing:  # If a bundle with the title 'name' already exists.
            logger.warning("A bundle with the title '%s' already exists." % name)
            stop = raw_input("Continue? (y/n)").lower()
            if stop != 'y':
                logger.info("Cancelled the order to add the '%s' bundle, because it already existed." % name)
                return


        bundle = Bundle()
        bundle.name = name
        logger.debug("Created a '%s' bundle." % name)

        session.add(bundle)
        logger.debug("Added the %s bundle to the session" % name)

        self.bundles.append(bundle)
        logger.debug("Added the %s bundle to the instance list of bundles." % name)

        session.commit()
        logger.debug("Made a commit to the session.")

        return bundle

    def remove_bundle(self, bundle=None, name=None):
        """Removes a bundle from self.bundles, and **does not** delete bundle from database.

Args*

bundle is a bundle object, which will be removed

name is a bundle.name string, which will be queried and removed.
"""        

        try:
            self.bundles.remove(bundle)
            logger.info("Removed the %s bundle from %s" % (bundle.name, self.username))

        except ValueError:
            logger.error("Bundle('%s') does not exist." % bundle.name)

    def delete_bundle(self, bundle=None, name=None):
        """Removes a bundle from self.bundles, and *does* delete bundle from database.

Args*

bundle is a bundle object, which will be removed

name is a bundle.name string, which will be used
to query the bundle object, and then remove+delete.
"""

class Bundle(Base):
    __tablename__ = 'bundle'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    name = Column(String)

    flashcards = relationship("Flashcard")  # List
    user_id = Column(Integer, ForeignKey('user.id'))  # If no relationship - null

    def __repr__(self):
        return "<Bundle of '%s' flashcards>" % self.name

    def __init__(self):
        from datetime import datetime

        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    question = Column(String)
    answers = Column(PickleType)

    bundle_id = Column(Integer, ForeignKey('bundle.id'))

    def __repr__(self):
        return "<Flashcard(%s)>" % self.question[:20]  # First 20 chars

    def __init__(self):
        from datetime import datetime

        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime


Base.metadata.create_all(engine)  # init table?
