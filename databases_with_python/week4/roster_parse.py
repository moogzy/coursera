#!/usr/bin/python

'''

Coursera - Week 4 (Many-to-Many Relationships in SQL)

Parse roster in json format and create a relational database
which stores mappings of course to users and their roles.

Author: Adrian Arumugam
Date: 01-01-2016

'''

import json
import sqlite3

# Create db connection and grab cursor
dbconn = sqlite3.connect('rosterdb.sqlite')
dbcur = dbconn.cursor()

# Table preparation
#
# Member table models many to many relationship and
# uses primary key formed from ID in User and Course tables
dbcur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# Give the option of entering another json roster file
# otherwise default to roster_data.json
roster_file = raw_input('Please enter the file name of the roster: ')
if len(roster_file) < 1:
    roster_file = 'roster_data.json'

# Open file and load it into json.loads to get a string of lists
roster_data = open(roster_file).read()
json_roster = json.loads(roster_data)

# Parse the json data
#
# Set common names for entries in each list
for entry in json_roster:
    name,title,role = entry[0],entry[1],entry[2]

    print '%s,%s,%s' % (name,title,role)
   
    # Database munging - add entries to User, Course and Member tables where
    # relevant.
    dbcur.execute('''INSERT OR IGNORE INTO User (name)
          VALUES ( ? )''', ( name, ) )
    dbcur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    # Fetch the id from the matching row to use as primary key in Member table
    user_id = dbcur.fetchone()[0]
    
    dbcur.execute('''INSERT OR IGNORE INTO Course (title)
          VALUES ( ? )''', ( title, ))
    dbcur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    # Fetch the id from the matching row to use as primary key in Member table
    course_id = dbcur.fetchone()[0]

    dbcur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role)
          VALUES ( ?, ?, ? )''', ( user_id, course_id, role ) )

# Commit changes to database and close connection
dbconn.commit()
dbcur.close()
