"""Callables for flashcards"""

from models import session, Bundle, Flashcard



def show_bundles():
    "Returns a list of all of the bundles in the db."
    
    bundles = session.query(Bundle).all()
    return bundles

def show_flashcards():
    "Returns a list of all of the flashcards in the db."
    
    flashcards = session.query(Flashcard).all()
    return flashcards
        
def delete_bundle(name, all=False):
    """For deleting bundles (of flashcards).

    Has one **optional** argument
    
    all (False):
       If activated, will delete every bundle of flashcards.
    """
    if not all:
        session.delete(name)
        session.commit()
        
    if all:
        for flashcard_bundle in session.query(Bundle).all():
            session.delete(flashcard_bundle)
        session.commit()
    
def delete_flashcard(name, all=False):
    """For deleting flashcards.

    Has one **optional** argument
    
    all (False):
       If activated, will delete every flashcard.
    """
    if not all:
        session.delete(name)
        session.commit()
        
    if all:
        for flashcard_bundle in session.query(Bundle).all():
            session.delete(flashcard_bundle)
        session.commit()

