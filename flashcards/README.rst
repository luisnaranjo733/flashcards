Package index
=============

models.py
---------

This is where all of the sqlalchemy models are stored,
as well as any project settings.

This file is used for testing as well, with some pre built
instances that are only supposed to be created in debug mode.

flashcards.py
-------------

This is the actual leitner system for quizzing the user appropriately.

authenticate.py
---------------

This is used to authenticate, create, and remove users.

ui.py
-----

This is **strictly** user interface.

This will tie all of the other code together.

It will be made a console script when packaged.
