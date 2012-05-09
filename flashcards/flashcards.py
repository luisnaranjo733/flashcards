from models import session, Set, Flashcard

def create_set(name=None):
    "Creates a Flashcard object, saves it, and returns it"
    
    if not name:
        name = raw_input("Set name: ")
    flashcard_set = Set()
    flashcard_set.name = name
    
    session.add(flashcard_set)
    session.commit() #TODO: Remove this and wrap it in a recursive code block - when available.
    return flashcard_set

def show_sets():
    "Returns a list of all of the sets in the db."
    
    sets = session.query(Set).all()
    return sets

def show_flashcards():
    "Returns a list of all of the flashcards in the db."
    
    flashcards = session.query(Flashcard).all()
    return flashcards
        
def delete_set(name, all=False):
    """For deleting sets (of flashcards).

    Has one **optional** argument
    
    all (False):
       If activated, will delete every set of flashcards.
    """
    if not all:
        session.delete(name)
        session.commit()
        
    if all:
        for flashcard_set in session.query(Set).all():
            session.delete(flashcard_set)
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
        for flashcard_set in session.query(Set).all():
            session.delete(flashcard_set)
        session.commit()

