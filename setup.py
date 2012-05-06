try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name = "flashcards",
    version = "2.4",
    author = "Jose Luis Naranjo Gomez",
    author_email = "luisnaranjo733@hotmail.com",
    description = ("A simple command line flashcards utility, similar to physical flashcards."),
    license = "GNU GPL",
    install_requires= ['argparse','configobj',],
    entry_points = {
    'console_scripts': ['flashcards = flashcards.flashcards:main']
    },
    package_data = {'': ['*.txt']},
    keywords = "study flashcard replacement command line utility",
    url = "https://launchpad.net/pyflashcards",
    packages=['flashcards'],
    long_description=read('README.txt'),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Utilities",
    ],
)
    
