#!/usr/bin/python

"""

Using Databases with Python - Coursera

Parsing raw email headers to obtain organization email domains
and place them into a database with their appearance count.

Author: Adrian Arumugam (apa@moogzy.net)
Date: 23-12-2015

"""

import urllib
import re
import sqlite3

# Regex to match email domain.
email_re = r'\w+@(.+)'

# Query to get email domain with most email. Ordered by 'count'
query_sql = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

# Open site to retrieve website data, read into variable and then
# split this into lines for parsing.
opensite = urllib.urlopen('http://www.pythonlearn.com/code/mbox.txt')
webdata = opensite.read()
weblines = webdata.splitlines(True)

# Open database connection and grab the db cursor
dbconn = sqlite3.connect('countorg.sqlite')
dbcur = dbconn.cursor()

# Drop the table if it exists at run time.
dbcur.execute('''
	DROP TABLE IF EXISTS Counts''')

# Create a fresh table after the DROP has completed.
dbcur.execute('''
	CREATE TABLE Counts (org TEXT, count INTEGER)''')

# If our webdata was empty - print a message and quit.
if len(weblines) <= 0:
	print 'Web data was empty - nothing to process'
	pass
else:

	# Variable to count how many 'interesting' lines we process
	linecount = 0

	# Process each line of webdata, we're only interested in those that
	# start with 'From'.
	for line in weblines:
		if not line.startswith('From: '):
			continue
		linecount += 1

		# Grab the organization domain from the email address
		# return a list with the matched objects.
		orgdomain = re.findall(email_re, line)

		# Query the database for entries relating to the current 'orgdomain'
		dbcur.execute('SELECT count FROM Counts WHERE org = ? ', (orgdomain[0], ))
		row = dbcur.fetchone()

		# If the query response was empty then we need to insert this 'orgdomain'
		# into the database, do so with a value of 1. If the sql query did return
		# data then we simply perform an update on the respective org row and increment
		# its count by 1.
		if row is None:
			dbcur.execute('''INSERT INTO Counts (org, count) VALUES ( ?, 1 )''', (orgdomain[0], ))
		else:
			dbcur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (orgdomain[0], ))
	
	# Try and except block for the database commit.
	# Print how many 'interesting' lines of text parsed.
	try:
		dbconn.commit()
		print 'Processed %d lines' % (linecount)
		print 'Database commit complete'
	except:
		print 'Database commit failed'

# Print out data from sql query. Use try\except block in case the database
# is empty.
print
print "Counts:"
try:
	for row in dbcur.execute(query_sql):
		print str(row[0]), row[1]
except:
	print 'Could not execute database query'

# Close out database connection.
dbcur.close()