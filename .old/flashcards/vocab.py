import os
from sys import platform,argv
from dictionary import search
from db_api import db_op

try:
    fname = argv[1]
except IndexError:
    print "Needs argv1 of fname containing vocab words to function! OR re-write top lines of code in %s." % os.path.dirname(os.abspath(__file__)) #Check this

try:
    table = argv[2]
except IndexError:
    print "Assuming 'misc' as table for flashcards"
    table = 'misc'

txt = open(fname,'r+')
words = txt.readlines()
txt.close()

home_path = os.path.expanduser("~")
if platform == 'linux2' or platform == 'darwin':
    documents = os.path.join(home_path, 'Documents')
    ROOT = os.path.join(documents, 'flashcards')
    

if platform == 'win32':
    documents = os.path.join(home_path, 'Documents')
    ROOT = os.path.join(documents, 'flashcards')
    
if not os.path.isdir(ROOT):
    os.mkdir(ROOT)
    
db_path = os.path.join(ROOT, "flashcards.db")

db = db_op(db_path)
if not table:
    table = 'misc'
info =  db.read_from_tbl(table)
def current_id():
    current = []
    for entry in info:
        ID = entry[0]
        current.append(ID)
    current.sort()
    try:
        return current[-1]
    except:
        return 0

#write_to_tbl(self, ID, question, answer, selection=None)
def write():
    for word in words:
        next_id = current_id()+1
        results = search(word)
        definition = results[1]
        db.write_to_tbl(next_id,word,definition,selection=table)
        print "Adding %s to database..." % word

    print "Done!"

write()

db.close()
