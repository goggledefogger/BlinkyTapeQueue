#!/usr/bin/env python
import pika
import logging
import blinkycommands
import lifeline
import datetime
import urlparse

logging.basicConfig()

logger = logging.getLogger('blinkylog')
if not logger.handlers:
    hdlr = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

def addCommandToQueue(command):
	commandConnection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',
																																	heartbeat_interval=1))
	commandChannel = commandConnection.channel()
	commandChannel.queue_declare(queue='blinkytape')
	commandChannel.basic_publish(exchange='',
	                      routing_key='blinkytape',
	                      body=command)
	commandConnection.close()
	logger.info("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Added '"+ command + "' command to queue")
	
def messageReceived(ch, method, properties, body):
	logger.info("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Received %r" % (body,))
	command = body.lower().strip()
	if command.startswith("'"):
		command = command.replace("'", "")

	if command.startswith("calendar"):
		options = command.split("calendar ",1)[1]
		optionsParams = urlparse.parse_qs(options)
		date = optionsParams['date'][0]
		id = optionsParams['id'][0]
		lifeline.addCalendarEvent(id, date)
	elif command == "on":
		blinkycommands.turnLightsOn()
	elif command == "blazers_start":
		blinkycommands.blazersLights()
	elif command == "snowing":
		blinkycommands.snowingLights()
	elif command == "camera_triggered":
		blinkycommands.snowingLights()
	else:
		logger.info('unrecognized command, just turn them on')
		blinkycommands.turnLightsOn()
	
def startListening(callback):
	connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
	logger.info(' [*] Waiting for messages. To exit press CTRL+C')
	channel = connection.channel()
	channel.queue_declare(queue='blinkytape')
	channel.basic_consume(callback,
		              queue='blinkytape',
		              no_ack=True)
	channel.start_consuming()
	

if __name__ == '__main__':
	startListening(messageReceived)
