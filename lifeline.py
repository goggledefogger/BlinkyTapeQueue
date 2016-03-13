#!/usr/bin/env python

from BlinkyTapeV2 import BlinkyTape
import logging
import time
import glob
import os
import pickle
import datetime

logging.basicConfig()

serialPorts = glob.glob("/dev/ttyACM*")
port = serialPorts[0]
bt = BlinkyTape(port)

storageFileName = 'lifeline.p'
tickTime = 0.01

# the format of the data will be:
# {
# 	'eventsById': {
# 		<id>: {
# 			'id': <id>,
# 			'date': <timestamp>
# 		}
# 	},
# 	'eventsByWeek': {
# 		<weekIndex>: {
# 			0: {
# 				<timestamp>: <id>,
# 				<timestamp>: <id>,
# 				...
# 			},
# 			1: {

# 			},
# 			...,
# 			6: {

# 			}
# 		}
# 	}	
# }
lifelineMap = {
	'eventsById': {},
	'eventsByWeek': {}
}
loaded = False

def start():
	diskData = loadFromFile()
	if (diskData is not None):
		lifelineMap = diskData
	loaded = True

def addCalendarEvent(id, unixDateString):
	if (not loaded):
		start()
	unixDate = int(unixDateString)
	lifelineMap['eventsById'][id] = {'id': id, 'date': unixDate}
	weekIndex = calculateWeekIndex(unixDate)
	dayIndex = calculateDayIndex(unixDate)
	print dayIndex
	if weekIndex not in lifelineMap['eventsByWeek']:
		lifelineMap['eventsByWeek'][weekIndex] = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}} 
	
	if unixDate not in lifelineMap['eventsByWeek'][weekIndex][dayIndex]:
		lifelineMap['eventsByWeek'][weekIndex][dayIndex][unixDate] = {}

	lifelineMap['eventsByWeek'][weekIndex][dayIndex][unixDate] = id
	saveToFile(lifelineMap)
	startCalendarLights()

def calculateWeekIndex(unixDate):
	dateObj = datetime.date.fromtimestamp(unixDate)
	return int((dateObj - datetime.date.min).days / 7)

def calculateDayIndex(unixDate):
	dateObj = datetime.date.fromtimestamp(unixDate)
	return dateObj.weekday()

def startCalendarLights():
	stop = time.time() + 10

	while time.time() < stop:
		# Run a tick on each block
		for i in range(0,bt.getSize()):
			bt.setPixel(i,255,123,10)
		bt.sendUpdate()

		time.sleep(tickTime)

	for i in range(0,bt.getSize()):
		bt.setPixel(i,0,0,0)
	bt.sendUpdate()

def loadFromFile():
	if os.path.exists(storageFileName):
		return pickle.load(open(storageFileName, "rb"))
	else:
		return None

def saveToFile(data):
	pickle.dump(data, open(storageFileName, "wb"))
	print data


start()
