Copyright (c) 2012 Jose Luis Naranjo Gomez
  This file is part of Flashcards

    Flashcards is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Flashcards is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Flashcards.  If not, see <http://www.gnu.org/licenses/>.
========================================================================

Flashcards is meant to be called from the command line.

Type "flashcards --help"into the command line once you've installed it.

========================================================================
GENERAL USAGE
========================================================================
Once you've installed the program
    1) Open up 'cmd' if you are on Windows computer, or the 'terminal' if you are
    on a Mac or Linux computer.
    2) Enter "flashcards" or "flashcards --help" for more info.

When you are adding answers in the program, you can add multiple choices.
    Seperate every possible answer with a comma.
    
NOTE:    
    Flashcards creates a folder in your Documents folder regardless of your OS.
    It is called "flashcards" and inside of it are two files:
    
    1) defaults.conf - You add true or false values
    for whichever data method your prefer. This allows you to bypass the
    root menu whenever you call flashcards.
    
    Example defaults.conf contents:
        csv=false
        sql=true
    
    This would have the program start in sql mode automatically, unless
    you specify that you want the csv version with the csv flag (--csv).
    
    
    2) flashcards.db
        This is created the first time you use the sqlite3 version of flashcards.
        This is where the "sets" of flashcards are stored.
    
CSV MODE AND SQL MODE

1) CSV - Comma Separated Values
This mode creates a data.csv file in the current working directory.

Advantages:
    Easier to edit by yourself - without the program
    More portable
    
If you want to edit your flashcards yourself:
    Open the data.csv file, which is probably in your home folder.
    Each line contains a question and it's answer/s.
    The first value is the question, and the rest of the values in that
        line are the answers.
    Each value is separated by commas. Spacing matters, so be careful.

2) SQL - Database storage
This mode creates a ".flashcards.db" file in your home folder.

Advantages:
    Allows for storing SETS of flashcards.
    Provides a more advanced editor.
    Better for long term storage.

========================================================================
CHANGESv2.3.1 (Current)
========================================================================
1) Moved root folder to Documents folder on Mac, Windows, and Linux
2) Moved data.csv there instead of cwd, and renamed it flashcards.csv
3) Made some aesthetic improvements with csv quiz
4) Fixed a major bug that had not been detected with the csv quiz


========================================================================
CHANGESv2.3
========================================================================
1) Created a folder for flashcards in the user's home directory. It is c
alled ".flashcards" - so it is hidden from view on Mac and Linux compute
rs. Inside this file is the .flashcards.db and defaults.conf file.
2) Added a defaults.conf file in ~.flashcards/

========================================================================
CHANGESv2.2
========================================================================
1) MAJOR: Implemented sqlite3 database option.
2) initial menu asks if the user wants a sqlite3db in their home directo
ry OR a csv file in their cwd.
3) This leads them to the corresponding quiz. This means that there are 
two bundled version of the quiz. 
4) The quiz_sql.py script relies on db_api, a script a sqlite3 framework
class designed for the quizzes' use.
5) Implemented csv.writer to writer() class in quiz_csv.
6) Switching zipped lists to a dictionary in csv quiz.
7) Added flags for CLI args.


========================================================================
CHANGESv2.0
========================================================================
1) Implemented CSV.reader succesfully to reader class. Data is stored in
    data.csv now.
2) Collapsed quiz_creator.py and quiz.py into quiz.py - they are both no
w classes.
3) Updated documentation.
4) Brought back __main__.py
5) Commented important code
6) No known bugs

========================================================================
CHANGESv1.2
========================================================================
1) Removed append mode (write only now).
2) Reverted a bunch of changes - flashcards just wasn't ready yet for th
    implementations.
    
========================================================================
CHANGESv1.1
========================================================================
1) Added append mode for quiz_maker.py and gave it a menu.
2) Fixed incorrect package name in README.txt
3) Moved menu.py to __init__.py
4) Added line breaks to menu UI in __main__.py
5) Improved error handling with semantic errors.
6) Improved documentation
7) Commented on some code

========================================================================
FUTURE IDEAS
========================================================================
1) Provide sound and graphics with pygame
2) Provide a cross-platform GUI with pyGTK+
3) Provide a browser version with Django


========================================================================
REQUIRES
========================================================================
argparse - for the --help menu and flags
configobj - for the default configuration file functionalities

Source: https://launchpad.net/pyflashcards or http://pypi.python.org/pypi/pyflashcards/2.2
