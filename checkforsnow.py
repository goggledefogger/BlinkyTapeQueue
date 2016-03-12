#!/usr/bin/env python

import queuemanager
import logging
import datetime
import time
import pickle
import os
import json
import urllib

checkIntervalInSeconds = 60*5

storageFileName = 'snow_level.p'
existingSnowLevel = 0
snowLevelMap = {}

logging.basicConfig()

logger = logging.getLogger('blinkylog')
if not logger.handlers:
    hdlr = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)


def getLastSnowLevelFromFile():

	if os.path.exists(storageFileName):
		snowLevelMap = pickle.load(open(storageFileName, "rb"))
		existingSnowLevel = snowLevelMap['new_snow']
	else:
		existingSnowLevel = 0
	return existingSnowLevel

def sendCommand(command):
	queuemanager.addCommandToQueue(command)
	
	
def checkForSnow():
	results = json.load(urllib.urlopen("http://www.kimonolabs.com/api/bzthkqyi?apikey=d58b2fd9039564d06471e14f3064f301"))
	newSnowString = results['results']['collection1'][0]['new_snow_string']
	newSnowString = newSnowString.lower().split("new snow past 12 hours:")[1].strip()
	existingSnowLevel = getLastSnowLevelFromFile()
	if existingSnowLevel == -1:
		snowLevelMap['new_snow'] = newSnowString
		existingSnowLevel = int(newSnowString)
	if int(newSnowString) > existingSnowLevel:
		logger.info("There was new snow!")
		logger.info("Current inches: " + newSnowString + ", last time checked inches: " + str(existingSnowLevel))
		sendCommand('snowing')
	snowLevelMap['new_snow'] = int(newSnowString)	
	pickle.dump(snowLevelMap, open(storageFileName, "wb"))
	
if __name__ == "__main__":

	logger.info("Scheduling snow checker...")
	while True:
		checkForSnow()
		time.sleep(checkIntervalInSeconds)
