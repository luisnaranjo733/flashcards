from models import *

history = Set()
ww2 = Flashcard()
answer = Answer()

ww2.question = 'When did WWII start?'

answer.answer = '1939'

ww2.answers.append(answer)


history.name = 'history'

history.flashcards.append(ww2)



session.add(ww2)
session.add(history)


session.commit()

if DEBUG:
    print "History flashcards:\t", history.flashcards
    print "Question of first flashcard:\t", history.flashcards[0].question
    print "Answer:\t", history.flashcards[0].answers[0].answer

