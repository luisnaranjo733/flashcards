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
from sys import platform
from configobj import ConfigObj


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
settings_path = os.path.join(ROOT, "settings.conf")
csv_path = os.path.join(ROOT,"flashcards.csv")

class conf(object):
    """
    Reads the settings file, and creates it with false values if it doesn't exist and sets vals to false if file empty.
    Returns a dict with booleans. conf.settings['csv'] and conf.settings['sql']
    Requires no parameters. Stand-alone. Assumes conf file is in hidden flashcards folder and is called 'defaults.conf'
    """
    def __init__(self,path=settings_path):
        self.home_path = os.path.expanduser("~")
        self.path = path
        self.file_exists = os.path.isfile(self.path)
        self.settings = dict()
        self.parse()
        self.clean()

    def parse(self):
    
        if self.file_exists:
            config = ConfigObj(self.path)
            
            try:
                csv = config['csv']
                sql = config['sql']
            except:
                csv = None
                sql = None
                self.file_exists = False
                
            self.settings['sql'] = sql
            self.settings['csv'] = csv
            
        if not self.file_exists:
            default = False
            config = ConfigObj()
            config.filename = self.path
            config['csv'] = default
            config['sql'] = default
            config.write()
            self.file_exists = True
            self.parse()

    def clean(self):
        settings = self.settings
        for keyword in settings:
            stop_words = "true false True False".split()
            value = settings[keyword]
            
            if value == 'true' or value == "True":
                settings[keyword] = True
                
            if value == 'false' or value == "False":
                settings[keyword] = False


