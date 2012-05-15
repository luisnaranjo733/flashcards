from pprint import pprint
from types import MethodType
from models import *

def get(obj):
    return session.query(obj).all()


def describe(obj):
    """Prints out general information about the model instance."""

    print "="*72, "\n", obj.__tablename__.upper().center(72), "\n", "="*72

    for attr in dir(obj):
        if attr[0] != '_' and attr != 'metadata':
            value = getattr(obj, attr)
            if isinstance(value, MethodType):
                try:
                    value = value()
                except TypeError:
                    value = value
            print("{attr}: {val}".format(attr=attr, val=value))

models = [User, Deck, Flashcard, CardBox]

def describe_all():
    for model in models:
        instances = get(model)
        for instance in instances:
            describe(instance)


