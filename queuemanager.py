#!/usr/bin/env python
import pika
import logging
import blinkycommands
import datetime

logging.basicConfig()

logger = logging.getLogger('blinkylog')
hdlr = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

def addCommandToQueue(command):
	commandConnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
	if command == "on":
		blinkycommands.turnLightsOn()
	elif command == "blazers_start":
		blinkycommands.blazersLights()
	elif command == "snowing":
		blinkycommands.snowingLights()
	else:
		logger.info('unrecognized command, just turn them on')
		blinkycommands.turnLightsOn()
	
def startListening(callback):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	logger.info(' [*] Waiting for messages. To exit press CTRL+C')
	channel = connection.channel()
	channel.queue_declare(queue='blinkytape')
	channel.basic_consume(callback,
		              queue='blinkytape',
		              no_ack=True)
	channel.start_consuming()
	

if __name__ == '__main__':
	startListening(messageReceived)
