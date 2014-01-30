#!/usr/bin/env python

print "importing"

import feedparser
print "1"
import queuemanager
import logging
import datetime
import time
print "2"
import pickle
import os
import imaplib
from email.parser import HeaderParser
print "3"
import json
import urllib
import pushimap
import sched
import threading

print "done importing"

imap_server = 'imap.gmail.com'


logging.basicConfig()

USERNAME = "blinkytape@gmail.com"
PASSWORD = "helloroy"

storageFileName = 'completed_commands.p'

if os.path.exists(storageFileName):
	completedCommands = pickle.load(open(storageFileName, "rb"))
else:
	completedCommands = {}

def sendCommand(command):
	queuemanager.addCommandToQueue(command)
	
	
def markCommandMailAsRead(conn, uid):
	data = conn.uid('store',uid,'-FLAGS','\\Seen')
	print 'Marked mail ' + uid + 'as read'
	
def newMailFound():
	checkMailForNewCommands()

def finish():
	print "finished"

def checkMailForNewCommands():
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': checking gmail for commands...'
	conn = imaplib.IMAP4_SSL(imap_server)

	try:
	    (retcode, capabilities) = conn.login(USERNAME, PASSWORD)
	except:
	    print sys.exc_info()[1]
	    sys.exit(1)

	conn.select() # Select inbox or default namespace
	(retcode, messages) = conn.uid('search', None, '(UNSEEN)')
	if retcode == 'OK':
	    for uid in messages[0].split():
		print 'Found an undread message with id: ' + uid
		data = conn.uid('fetch', uid, '(BODY[HEADER])')
		header_data = data[1][0][1]
		parser = HeaderParser()
		msg = parser.parsestr(header_data)
		subjectText = msg["Subject"].lower()

		if not subjectText.startswith("[command]"):
			continue
			
		# if we've already processed this email, move on
		if uid in completedCommands:
			continue
		
		commandString = subjectText.split("[command]")[1].strip()
		completedCommands[uid] = commandString
		markCommandMailAsRead(conn, uid)
		sendCommand(commandString)
	
	pickle.dump(completedCommands, open(storageFileName, "wb"))
	conn.close()


if __name__ == "__main__":
	checkMailForNewCommands()
	pushimap.startListening(USERNAME, PASSWORD, newMailFound)

