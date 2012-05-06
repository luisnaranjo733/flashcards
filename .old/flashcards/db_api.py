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

import os
import sys
import sqlite3

class db_op(object):
    def __init__(self,path):
        
        self.db_path = path

        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()
        self.tables_exist = False
        self.index = self.get_index() #List of tables in the database
        
    def refresh(self): #Working
        """Reload the initializer for more up to date information"""
        
        self.__init__(self.db_path)

    def close(self): #Working
        """For simple connection closing"""
        
        self.con.close()
        
    def get_index(self): #Working
        """Returns a list of all of the tables in the database"""
        
        sqlite_master = self.cur.execute("SELECT name FROM sqlite_master")
        index = []
        for table in sqlite_master:
            if table:
                self.tables_exist = True
            index.append(table[0])
        return index

    def select_tbl(self,msg="select",disp=True): #Working
        """Returns the name of the table that the user specifies. Depends on the get_index method"""
        
        self.refresh()
        if disp:
            print "Which table would you like to %s?" % msg
            
        count = 1
        tbl_track = [None]
        for table in self.index:
            if not table or table == '': #Not working
                print "No tables available!"
                
            print "%d:\t%s"% (count,table)
            tbl_track.append(table)
            count += 1
        try:
            selection = raw_input("> ")
            if selection == "exit" or selection == 'end':
                self.close()
                sys.exit(0)
                
            selection = int(selection)
        except ValueError:
            print("You need to tell me which set of flashcards you want to %s!" % msg)
            self.close()
            sys.exit(0)
            
        return tbl_track[selection]
        
    def delete_tbl(self, selection=None): #Working
        """Deletes the table that the user specifies in the select_tbl method, if it exists."""
        self.refresh()
        
        if not selection:
            selection = self.select_tbl("delete")
        
        try:
            self.cur.execute("drop table %s" % selection)
        except sqlite3.OperationalError:
            print "%s doesn't exist!" % selection
        self.con.commit()
        
    def create_tbl(self,name = None): #Working
        """Creates a user-named table with default parameter"""
    
        if not name:
            print "What would you like to name your table?"
            name = raw_input("> ")
            
        try:
            self.cur.execute("create table if not exists %s(id integer, question text, answer text)" % name)
            print "Created table if it didn't exist:\t%s" % name
        except sqlite3.OperationalError:
            print "SQLITE DATABASE ERROR"
            print "Make sure your database name has no spaces or odd characters!"
        self.con.commit()
        self.refresh()
        

        
    def delete_all(self): #Working
        """WARNING: Deletes all of the tables in the database!"""
        
        self.refresh()
        for table in self.index:
            self.delete_tbl(table)
            
    def write_to_tbl(self, ID, question, answer, selection=None):
        """Writes three values (1st 2nd and 3rd parameters) to the given table (4th optional parameter)
        If not table is given, activates select_tbl menu"""
    
        if not selection:
            selection = self.select_tbl("write to")
            
        sql_stmt = "insert into %s values(?,?,?)" % selection
        self.cur.execute(sql_stmt, (ID, question, answer))
        self.con.commit()
        self.refresh()
    
    def read_from_tbl(self, table=None):
        """Reads from the given table. Provides an alternate menu (select_tbl) if no table is given."""
        if not table:
            table = self.select_tbl("read from")
        
        reader = self.cur.execute("select * from %s" % table)
        values = []
        for row in reader:
            ID = row[0]
            question = row[1]
            answer = row[2]
            
            format = (ID,question,answer)
            values.append(format)
        return values
        
    def print_values(self, table):
        """Prints out all of the values in the given table."""
        
        entries = self.read_from_tbl(table)
        for entry in entries:
            ID = entry[0]
            question = entry[1]
            answer = entry[2]
                
            print "ID:      \t%s" % ID
            print "Question:\t%s" % question
            print "Answer:  \t%s\n" % answer
        
            
    def delete_from_tbl(self, table=None, value=None):
        """Deletes the selected value from the given table."""
        
        if not table:
            table = self.select_tbl("delete from")
            
        if not value:
            self.print_values(table) #Prints out the values in the table
            
            print "Which value in %s would you like to delete?" % table

            value = int(raw_input("ID:\t"))
            
        self.cur.execute("delete from %s where id==%s" % (table,value))
        print "Deleted question number %d." % value
        self.con.commit()
            

        
        

#db = db_op()

#db.refresh() #Reloads db info

#print db.index #List of all of the tables in the db
#db.select_tbl(msg) #Menu for choosing a table in the db, returns table name

#   TABLE METHODS
#db.create_tbl(name) #Creates a table in the db
#db.delete_tbl(name=None) #Deletes a table in the db
#db.delete_all() #Deletes all of the tables in the db

#   VALUE METHODS
#db.write_to_tbl(id,question,answer,table) #For inserting values to a table
#db.read_from_tbl(table=None) #Retuns list of tuples from that table. Each tuple is a set -  (id, question, answer)
#db.delete_from_tbl(table=None) #Deletes a value in the table
#db.print_values(table=None) #Prints all of the values in the table

#db.con.commit()
#db.close()
#list_tables() #Lists all available tables
