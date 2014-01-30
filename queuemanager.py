#!/usr/bin/env python
import pika
import logging
import blinkycommands
import datetime

logging.basicConfig()

def addCommandToQueue(command):
	commandConnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	commandChannel = commandConnection.channel()
	commandChannel.basic_publish('',
	                      'blinkytape',
	                      command,
	                      pika.BasicProperties(content_type='text/plain',
                                               delivery_mode=1))
	commandConnection.close()
	print "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Added '"+ command + "' command to queue"
	
def messageReceived(ch, method, properties, body):
	print "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Received %r" % (body,)
	command = body.lower().strip()
	if command == "on":
		blinkycommands.turnLightsOn()
	elif command == "blazers_start":
		blinkycommands.blazersLights()
	elif command == "snowing":
		blinkycommands.snowingLights()
	else:
		blinkycommands.turnLightsOn()
	
def startListening(callback):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	print ' [*] Waiting for messages. To exit press CTRL+C'
	channel = connection.channel()
	channel.basic_consume(callback,
		              queue='blinkytape',
		              no_ack=True)
	channel.start_consuming()
	

if __name__ == '__main__':
	startListening(messageReceived)
