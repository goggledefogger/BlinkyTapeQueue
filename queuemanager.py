#!/usr/bin/env python
import pika
import logging
import blinkycommands
import datetime

logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='blinkytape')

def addCommandToQueue(command):
	
	channel.basic_publish(exchange='', routing_key='blinkytape', body=command)
	print "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Added '"+ command + "' command to queue"
	
def messageReceived(ch, method, properties, body):
	print "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Received %r" % (body,)
	command = body.lower().strip()
	if command == "on":
		blinkycommands.turnLightsOn()
	if command == "blazers_start":
		blinkycommands.blazersLights()
	if command == "snowing":
		blinkycommands.snowingLights()
	else:
		blinkycommands.turnLightsOn()
	
def startListening(callback):

	print ' [*] Waiting for messages. To exit press CTRL+C'


	channel.basic_consume(callback,
		              queue='blinkytape',
		              no_ack=True)

	channel.start_consuming()
	

if __name__ == '__main__':
	startListening(messageReceived)
