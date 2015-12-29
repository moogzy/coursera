#!/usr/bin/python

"""

Coursera - Using Databases with Python

Week 3

Creating a music track database from XML file

Author: Adrian Arumugam
Date: 29-Dec-2015

"""

import xml.etree.ElementTree as ET
import sqlite3

# Open DB connection and grab the cursor
dbconn = sqlite3.connect('trackdb.sqlite')
dbcur = dbconn.cursor()

# Make some fresh tables using executescript()
dbcur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Initialize XML file
trackfile = raw_input("Please enter the tracks filename: ")

# Set default file name if .xml doesn't exist
if ".xml" not in trackfile:
  trackfile = 'tracks/Library.xml'

# Open XML file with element tree and look for
# third layer of dictionaries which hold the track information
trackxml = ET.parse(trackfile)
trackdict = trackxml.findall('dict/dict/dict')

# Function which allows lookup within a ET dictionary element 
# to find given key and return the next corresponding text
#
# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
#
# For example after key:Name, next text is strin:Another One bites the Dust.
def entrylookup(entry, key):
    found = False
    for child in entry:
        if found: 
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

# Parse each item in trackdict and send it to function for 
# key lookup.
for item in trackdict:
    # If Track ID is None then we don't need to go further
    # skip forward to next item.
    if ( entrylookup(item, 'Track ID') is None ):
        continue
    title = entrylookup(item, 'Name')
    artist = entrylookup(item, 'Artist')
    album = entrylookup(item, 'Album')
    genre = entrylookup(item, 'Genre')
    length = entrylookup(item, 'Total Time')
    rating = entrylookup(item, 'Rating')
    count = entrylookup(item, 'Play Count')
    
    # If any of these variables are None then skip to next item
    if title is None or artist is None or album is None:
        continue
    
    # This line is more for debugging, leave here for completeness
    print title,artist,album,genre,length,rating,count

    # Try\Except blocks to execute DB instructions

    # Enter Artist details into the Artist table and
    # grab the artist ID integer.
    #
    # Must be unique so ignore if Artist already exists.
    try:
        dbcur.execute('''INSERT OR IGNORE INTO Artist (name) 
              VALUES ( ? )''', ( artist, ) )
        dbcur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
        artist_id = dbcur.fetchone()[0]
    except:
        print "Entering name into database has(Artist) has failed."

    # Enter Album details in the Album table and grab the album ID integer
    #
    # Must be unique so ignore if Album already exists.
    # 
    # Linked to artist table via the 'Artist_ID' variable
    try:
        dbcur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
              VALUES ( ?, ?)''', ( album, artist_id ) )
        dbcur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
        album_id = dbcur.fetchone()[0]
    except:
        print "Entering title,artist_id into database(Album) has failed."

    # Enter Genre details into the Genre table and grab the genre ID integer
    #
    # Must be unique so ignore if Genre already exists.
    try:
        dbcur.execute('''INSERT OR IGNORE INTO Genre (name)
              VALUES ( ? )''', ( genre, ) )
        dbcur.execute('SELECT id from Genre WHERE name = ? ', (genre, ))
        genre_id = dbcur.fetchone()[0]
    except:
        print "Entering name into database(Genre) has failed."

    # Enter track details into the Track table.
    #
    # Links back to album, artist, genre tables.
    #
    # If track already exists we simply replace it.
    try:
        dbcur.execute('''INSERT OR REPLACE INTO Track
              (title, album_id, genre_id, len, rating, count)
              VALUES ( ?, ?, ?, ?, ?, ? )''',
              ( title, album_id, genre_id, length, rating, count ) )
    except:
        print "Entering track details into database(Track) has failed."
    
    # Commit new entries to database.
    dbconn.commit()

# Close out database connection cleanly.
dbconn.close()
