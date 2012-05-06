#!/usr/bin/env python

#Copyright (c) 2012 Jose Luis Naranjo Gomez
#    This file is part of Flashcards
#
#    Flashcards is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Flashcards is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Flashcards.  If not, see <http://www.gnu.org/licenses/>.

#adsjfbhadslfbaskjbaskdbf

from sys import exit, argv
import os
import argparse
import db_api
import quiz_csv
import quiz_sql
import configure
from configobj import ConfigObj

def set_default(value=False):
    config = ConfigObj()
    config.filename = configure.settings_path
    configure.conf()
    
    choice = None
    value = None
    if value:
        if value == "csv":
            choice = "1"
        if value == "sql":
            choice = "2"
            
    if not value:
        print configure.settings_path
        print "What would you like the default flashcard storage behaviour to be?"
        print "1:\tDatabase (More advanced - more features)"
        print "2:\tCsv file (You can edit this!)"
        choice = raw_input("> ")
        
    if choice == '1':
        config['csv'] = False
        config['sql'] = True
        
    if choice == '2':
        config['csv'] = True
        config['sql'] = False
    if not choice:
        configure.conf(configure.settings_path)
    if choice:
        config.write()
    exit(0)

def delete():
    print "Are you sure (Y/N)?"
    ask = raw_input("> ").lower()
    data_path = os.path.join(os.getcwd(), "data.csv")
    if ask == 'n' or ask == 'no':
        exit(0)
    else:
        txt = open(data_path, 'w')
        txt.truncate()
        txt.close()
        print "Erased '%s'." % data_path

def adder(table):
    breakers = "end exit break close leave stop".split()
    while True:
        question = raw_input("Question:\t")
        if question in breakers: 
            break
            
        answer   = raw_input("Answer  :\t")
        if answer in breakers:
            break
            
        quiz_sql.edit_set(question, answer,table)
        print "-"*72

def sub_menu_sqlite3(table):
    print "Loaded %s set of flashcards." % table
    print "="*72,"\n"
    breakers = "end exit break close leave stop".split()
    
    while True:
        print "\n\t%s MENU" % table.upper()
        print "1: Use flashcards" #Working
        print "2: Add flashcards" #Working
        print "3: Delete flashcards" #Working
        print "4: Go back to the main menu" #Working
        print "5: exit\n" #Working
        
        ask = raw_input("> ").lower()
        print "="*72
        
        if ask == '1':
            quiz_sql.use_set(table)
        
        if ask == '2':
            adder(table)
            
        if ask == '3':
            quiz_sql.db.delete_from_tbl(table)
        
        if ask == '4':
            break
        
        if ask in breakers or ask == '5':
            quiz_sql.close()
            
        print "="*72
def menu_sqlite3(load=None):
    print "Connected to %s" % quiz_sql.path
    print "="*72,"\n\n"
    
    if load:
        sub_menu_sqlite3(load)
        load = False
        
    if not load:
        while True:
            print "\tMAIN MENU"
            print "1: Load a set of flashcards" #Working
            print "2: Create a set of flashcards" #Working
            print "3: Delete a set of flashcards" #Working
            print "4: Delete all sets of flashcards" #Working
            print "5: exit\n" #Works
            
            ask = raw_input("> ").lower()
            #print "="*72

            if ask == 'list':
                for table in quiz_sql.db.index:
                    print table
                
            if ask == '1':
                table = quiz_sql.db.select_tbl("load")
                sub_menu_sqlite3(table)
                
            if ask == '2':
                quiz_sql.create_set()
                

            if ask == '3':
                table = quiz_sql.erase_set()
                print "Deleted %s set." % table
                
            if ask == '4':
                print "="*72
                print "Are you sure? (y\\n)"
                check = raw_input(">\n")
                if check.lower() == 'n':
                    print "="*72
                    continue
                if check.lower() == 'y':
                    quiz_sql.erase_all_sets()
                
            if ask.lower() == 'exit' or ask == 'end' or ask == '5':
                quiz_sql.close()
                
            print "="*72
def menu_csv():
    path = configure.csv_path
    print "Connected to %s." % path
    print "="*72
    while True:
        print "1: Enter quiz mode"
        print "2: Enter quiz editor"
        print "3: Erase current quiz"
        print "4: Exit"
        ask = raw_input("> ").lower()
        
       
        
        if ask == 'end':
            break
            
        if ask.lower() == 'exit' or ask == 'end' or ask == '4':
            exit(0)
            
        if ask == '1' or ask == "enter quiz mode":
            quizzer = quiz_csv.reader()
            quizzer.start()
            
        if ask == '2' or ask == 'enter quiz editor':
            writer = quiz_csv.writer()
            writer.start()
            
        if ask == '3' or ask == 'erase current quiz':
            delete()
            
        print "="*72
def get_args():
    parser = argparse.ArgumentParser(
        description="Purpose: A command line flashcard interface using both csv and sqlite3 modules",
        epilog="Developed by Luis Naranjo.\nSource is available at https://launchpad.net/pyflashcards/2.0"
    )

    parser.add_argument('-v','--version',  action='version', version='%(prog)s 2.4')

    parser.add_argument(
    '-c', '--csv',
    action='store_true',
    help="Use a csv file in the current working directory for storing data.",
    )

    parser.add_argument(
    '-s', '--sql',
    action='store_true',
    help="Use a sqlite3 database in your home directory for storing data.",
    )
    
    parser.add_argument(
    '-ls','--list',
    action='store_true',
    help="List all of the available sets of flashcards",
    dest="list",
    )
    
    parser.add_argument(
    '-rm', '--remove',
    help="Remove a set of flashcards",
    dest="remove",
    )
    
    parser.add_argument(
    '-l', '--load',
    help='Load a specific table of flashcards from sql db.',
    dest="load"
    )
    
    parser.add_argument(
    '-u', '--use',
    help="Use a set of flashcards",
    dest="use",
    )
    
    parser.add_argument(
    '-m', '--make',
    help="Make a set of flashcards",
    dest="make",
    )
    
    parser.add_argument(
    '-a', '--add',
    help="Add to a set of flashcards",
    dest="add",)
    
    parser.add_argument(
    '-d','--default',
    help="Set the default flashcard mode (csv/sql)",
    dest="default",
    )
    

    
    args = parser.parse_args()
    
    csv = args.csv
    sql = args.sql
    listy = args.list
    load = args.load
    use = args.use
    remove = args.remove
    make = args.make
    add = args.add
    default = args.default
    return (csv,sql,listy,load,use,remove,make,add,default)
    
    


def menu(args=get_args()):
    
    csv = args[0]
    sql = args[1]
    list = args[2]
    load = args[3]
    use = args[4]
    remove = args[5]
    make = args[6]
    add = args[7]
    default = args[8]
    
    if csv:
        menu_csv()
    if sql:
        menu_sqlite3()
    
    if list:
        index = quiz_sql.db.index
        count = 1
        print "Flashcard sets available:"
        for table in index:
            print "%d:\t%s" % (count,table)
            count += 1
        
    if load:
        menu_sqlite3(load)
        
    if use:
        quiz_sql.use_set(use)
        
    if remove:
        quiz_sql.db.delete_tbl(remove)
        #print "Deleted %s set." % remove
        
    if make:
        quiz_sql.db.create_tbl(make)
        
    if add:
        adder(add)
        
    if default:
    
        set_default(default)
        

    if not csv and not sql and not list and not load and not use and not remove and not make and not add:
        print "What type of data do you want to use?"
        print "1: Database"
        print "\tStores quizzes in database"
        print "2: CSV file"
        print "\tGenerates quiz file"
        print "3: exit"
        
        mode = raw_input("> ")
        
        if mode == 'end' or mode == 'exit' or mode == '3':
            exit(0)
        if mode == '1':
            menu_sqlite3()
        if mode == '2':
            menu_csv()


def main():
    data = configure.conf()
    mode = data.settings
    csv = mode['csv']
    sql = mode['sql']
    
    args = get_args()
    
    if args[0] or args[1]: #csv and sqlflag
        menu(args)
        exit(0)
        
    if (not sql and not csv) or (csv and sql):
        menu(args)
        
    if csv and not sql:
        menu_csv()
        
    if sql and not csv:
        menu_sqlite3()


if __name__ == "__main__":
    main()
