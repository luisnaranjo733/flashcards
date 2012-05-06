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
import csv
import configure

cwd = os.getcwd()
data_path = os.path.join(configure.ROOT,"flashcards.csv")

#Creates a data.csv file in the current working directory if it does not already exist.


class reader(object):
    """This class actually quizzes the user. It parses from data.csv which is created in the current working directory.
    It runs itself, so you just need to call reader() and it will read the data file in the cwd and quiz the user on it.
    """
    
    def __init__(self):
        open(data_path,'a')
        self.txt = open(data_path, 'r')
        self.reader = csv.reader(self.txt, delimiter=",")
        self.QNA = self.load(data_path) #Parses the information in ./data.csv and stores it in a dict.
        empty = self.check_for_empty_files()
        if empty:
            print "="*72
            print "The data.csv file is empty!"
        #self.start() #Gets the ball rolling.
        
    def msg(self,message):
        print "="*72
        print message
        
    def load(self,path):
        """Loads a CSV file returns a dict of answers/questions"""
        #Thanks to ath0 (http://www.reddit.com/user/ath0) who wrote this method from http://reddit.com/r/learnpython
        
        dataset = dict()
        with open(path, 'r') as f:
            for line in f.readlines():
                split_line = line.split(',')
                question = split_line[0]
                answers = split_line[1:]
                dataset[question] = answers
        return dataset
        
    def start(self):
        for q in self.QNA:
            question = q
            answers = self.QNA[q]
            
            if not question or not answers:
                continue
            
            self.msg("Question:\t%s" % question)
            attempt = raw_input("> ")
            
            for answer in answers:
                if attempt == answer:
                    correct = True
                    break
                else:
                    correct = False
            
            if correct:
                print "Correct!"
            if not correct:
                print "The correct answer was:"
                if len(answers) > 1:
                    print "\tany of the following:"
                    
                print "\t",' | '.join(answers)
                
        #print "="*72
        
    def check_for_empty_files(self):
        txt = self.txt.readlines()
        empty = True
        for line in txt:
            if line:
                empty = False
        return empty
                
#--------------------------------------------------------------------------------------------------------------------------------

class writer(object):
    """This class appends sets of questions and answers into the data.csv file
    in the current working directory. The reader() class above uses this file."""
    
    def __init__(self):
        open(data_path,'a')
        #File IO object in either 'a' or 'w' mode.
        self.txt = open(data_path,'a')
        #KEY is a list of tuples with strings in them. Each tuple is a pair of question and answer.
        self.KEY = self.get_key() #Gets the questions and answers from the user and stores them in self.KEY for self.start()
        #self.start() #Gets the ball rolling. write() is the function that actually writes information to ./data.csv
        
    def start(self):
        writer = csv.writer(self.txt)
        for q in self.KEY: #group is a tuple of strings
            question = "%s," % q #string+comma
            answers = self.KEY[q] #string
            
            format = question+answers # String with comma separated values. First value is question.
            format = format.split(",") #Split the format string at each comma into a list.
            
            writer.writerow(format)
            self.txt.write("\n")
        self.txt.close()


    def get_key(self):
    
        qna = {}
        
        print "="*72
        print "NOTE:\tSeparate multiple choice answers with commas."
        
        while True:
            print "="*72
            
            question = raw_input("Question:\t ")
            
            if question == 'exit' or question == 'end':
                break
            
            answer = raw_input("Answer/s:\t")
            if answer == 'exit' or answer == 'end':
                break
                

            qna[question] = answer
            
        print "\n"
        return qna
        
        
    def get_mode(self):
        print "1: Edit mode"
        print "2: Over-write mode"
        
        mode = raw_input("> ")
        
        cwd = os.getcwd()
        data_path = os.path.join(cwd, 'data.csv')
        txt = open(data_path,'a')
        if mode == '1' or mode == 'edit mode':
            txt = open(data_path,'a')
            mode = 'edit'
        if mode == '2' or mode == 'over-write mode':
            txt = open(data_path,'w')
            mode = 'over-write'
            
        print "Opening %s in %s mode..." % (os.path.join(os.getcwd(), 'data.csv'), mode)

        return txt
        

