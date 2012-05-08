from models import *




def show():
    "Takes a set - shows the questions and answers:"
    
if DEBUG:

    history = Set()
    ww2 = Flashcard()

    ww2.question = 'When did WWII start?'
    ww2.answers = ['1939']

    history.name = 'history'

    history.flashcards.append(ww2)



    session.add(ww2)
    session.add(history)

    session.commit()
    print "History (set) flashcards:\t", history.flashcards
    print "Question of first flashcard:\t", history.flashcards[0].question
    print "Answer:\t", history.flashcards[0].answers



def show_flashcards():
    flashcards = session.query(Flashcard).all()
    print flashcards
    for flashcard in flashcards:
        print "Question:\t",flashcard.question
        print "Answers?:\t",flashcard.answers
        
print "\n";show_flashcards()
