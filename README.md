# README #

BlinkyTape Queue

### What is this repository for? ###

* A python based messaging queue that will trigger light patterns on the BlinkyTape LED strip.
* Version 1.0

### How do I get set up? ###

* Connect the BlinkyTape with USB
* Start the message queue listening by running blinkystart.sh
* Uses the BlinkyTape python library modified [here](http://projects.mattdyson.org/projects/blinkytape/BlinkyTapeV2.py)
* Stop the message queue listening by running blinkystop.sh

### How do I add new light patterns? ###

1. Add the animation code in blinkycommands.py
2. Call that code either from an existing 'check' script (like checkforsnow.py or checkgmail.py), or create a new one

### Contribution guidelines ###

* Please contribute!

### Who do I talk to? ###

* Contact roy.town@outlook.com

### License ###

MIT
