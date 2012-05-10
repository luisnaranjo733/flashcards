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


class BundleError(Exception):
    """For catching errors that have to do with Bundle objects."""
    def __init__(self, error=None):
        self.error = error

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

    def add_bundle(self, name, repeat=False, ignore_repeat=False):  # Named args untested
        """Create a bundle of flashcards on an instance.

Args:

repeat: if true, a bundle will be added even if it already exists, without consent.
ignore_repeat: If true, and the bundle already exists, the function will just return None.

Returns the bundle object if it was created."""
        existing_bundle = session.query(Bundle).filter_by(name=name).first()

        # If a bundle with the title 'name' already exists.
        if existing_bundle in self.bundles and not repeat and not ignore_repeat:  # TODO: Document repeat and ignore_repeat
            logger.warning("A bundle with the title '%s' already exists." % name)
            stop = raw_input("Continue? (y/n)").lower()
            if stop != 'y':
                logger.info("Cancelled the order to add the '%s' bundle, because it already existed." % name)
                return

        if existing_bundle and ignore_repeat:  # TODO: Document ignore_repeat and what this block of code does.
            return

        bundle = Bundle()
        bundle.name = name
        logger.info("Created a Bundle('%s')" % name)

        session.add(bundle)
        logger.info("Added the Bundle('%s') to the session" % name)

        self.bundles.append(bundle)
        logger.info("Added the Bundle('%s') to the instance list of bundles." % name)

        session.commit()
        logger.info("Session commit")

        return bundle


    def delete_bundle(self, bundle_):
        """Removes a bundle from self.bundles, and *does* delete bundle from database.

Can take a persisted Bundle instance, or the self.name string of Bundle instance.

Raises a BundleError if bundle_ argument is invalid."""

        BundleInstance = isinstance(bundle_, Bundle)
        logger.debug("Is %s an instance of Bundle? %r" % (bundle_, BundleInstance))

        if BundleInstance:

            bundle = bundle_

        if not BundleInstance:  # Bundle var must be a Bundle.name of a Bundle instance
            try:
                bundle = session.query(Bundle).filter_by(name=bundle_).first()  # Get a bundle object using the given name.
                if not bundle:
                    raise BundleError

            except BundleError:
                logger.warning("'%s' is NOT a Bundle instance OR a Bundle instances' Bundle.name attribute!" % bundle_)
                logger.warning("Bundle.delete_bundle('%s') failed!" % bundle_)
                return

        try:
            self.bundles.remove(bundle)
            logger.info("Deleted the Bundle('%s') from User('%s')" % (bundle.name, self.username))

        except ValueError:
            logger.error("ValueError: Bundle('%s') does not exist." % bundle.name)

        session.delete(bundle)
        logger.info("Deleted the Bundle('%s') from the database registry" % bundle.name)

        session.commit()
        logger.info("Session commit")
            

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
    correct = Column(Integer)
    incorrect = Column(Integer)
    bundle_id = Column(Integer, ForeignKey('bundle.id'))

    def __repr__(self):
        return "<Flashcard('%s')>" % self.question[:40]  # First 20 chars

    def __init__(self):
        from datetime import datetime
        self.date_created = datetime.now()  # datetime.datetime object - converted back and forth from string
        del datetime
        self.correct = 0
        self.incorrect = 0

Base.metadata.create_all(engine)  # init table?

#TODO: REMOVE THIS AT ONCE
user = session.query(User).filter_by(username='luis').first()
