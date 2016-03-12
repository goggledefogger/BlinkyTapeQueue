#!/usr/bin/env python

import queuemanager
import logging
import sys

logging.basicConfig()

logger = logging.getLogger('blinkylog')
if not logger.handlers:
    hdlr = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)


if __name__ == "__main__":
  if len(sys.argv) <= 1:
    logger.info("You must specify a command")
  else:
    command = sys.argv[1]
    logger.info("Running a custom command " + command + "...")
    queuemanager.addCommandToQueue(command)
