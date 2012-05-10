Flashcards
==========

**Flashcards is under active development.**

What is it?
-----------

Flashcards is a simple memorization tool, written in **python**, which aims to emulate real flashcards.

The user can add “decks” of flashcards for different types of subjects, which are stored in a sqlite3 database. 

The user can then quiz his or herself on the flashcards.

How does it work?
-----------------

Flashcards is using the Leitner Algorithm, which focuses card repetition based on the most commonly missed cards.

More information on the Leitner Algorithm here: http://flashcarddb.com/leitner

Legacy code
-----------

Flashcards is a recently revived project (5/5/12)

Here is the old version: https://launchpad.net/pyflashcards

The older version was written messily, with manual SQL expressions, and the sqlite3 module.

This one will be a lot cleaner, and will depend on SQLAlchemy (0.7.7)
