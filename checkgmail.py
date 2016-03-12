#!/usr/bin/env python

import sys
import feedparser
import queuemanager
import logging
import datetime
import time
import pickle
import os
import imaplib
from email.parser import HeaderParser
import json
import urllib
import pushimap
import sched
import threading

imap_server = 'imap.gmail.com'

logging.basicConfig()

logger = logging.getLogger('blinkylog')
hdlr = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

logger.info("Starting gmail listener...")

USERNAME = "blinkytape@gmail.com"
PASSWORD = "blinkyroy"

storageFileName = 'completed_commands.p'

if os.path.exists(storageFileName):
	completedCommands = pickle.load(open(storageFileName, "rb"))
else:
	completedCommands = {}

def sendCommand(command):
	queuemanager.addCommandToQueue(command)
	
	
def markCommandMailAsRead(conn, uid):
	data = conn.uid('store',uid,'-FLAGS','\\Seen')
	logger.info('Marked mail ' + uid + 'as read')
	
def newMailFound():
	checkMailForNewCommands()

def finish():
	logger.info("finished")

def checkMailForNewCommands():
	logger.info('checking gmail for commands...')
	conn = imaplib.IMAP4_SSL(imap_server)

	try:
	    (retcode, capabilities) = conn.login(USERNAME, PASSWORD)
	except:
	    logger.error(sys.exc_info()[1])
	    sys.exit(1)

	conn.select() # Select inbox or default namespace
	(retcode, messages) = conn.uid('search', None, '(UNSEEN)')
	if retcode == 'OK':
	    for uid in messages[0].split():
		logger.info('Found an undread message with id: ' + uid)
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

