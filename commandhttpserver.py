#!/usr/bin/env python

import queuemanager
import logging
import time
import BaseHTTPServer
import re

logging.basicConfig()

logger = logging.getLogger('blinkylog')
if not logger.handlers:
    hdlr = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

HOST_NAME = ''
PORT_NUMBER = 9000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
  def do_GET(s):
      """Respond to a GET request: """ + s.path

      matchObj = re.match(r'\/lights\?command=(.*)', s.path)
      if matchObj:
        command = matchObj.group(1)
        logger.info('sending command: ' + command)
        queuemanager.addCommandToQueue(command)

      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write("<html><head><title>Command Received</title></head>")
      s.wfile.write("<body><p>Command received</p>")
      s.wfile.write("</body></html>")

if __name__ == '__main__':
  logger.info("Starting http listener...")

  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)