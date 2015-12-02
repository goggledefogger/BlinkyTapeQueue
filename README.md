# README #

BlinkyTape Queue

### What is this repository for? ###

* A python based messaging queue that will trigger light patterns on the BlinkyTape LED strip.
* Version 0.9

### How do I get set up? ###

* Create a Gmail account that can be used to trigger actions by email
* Update the Gmail username/password in checkgmail.py with your new credentials
* Connect the BlinkyTape with USB
* Start the message queue listening by running blinkystart.sh
* Use IFTTT (or any other service) to send emails to that account with the subject of the form:
[command] CommandString
and replace "CommandString" with the name you give to that command. So far the supported CommandStrings are "on", "blazers_start", and "snowing"
* Wait for snow, email, or Blazer games...and enjoy the show!
* Stop the message queue listening by running blinkystop.sh

Uses the BlinkyTape python library modified [here](http://projects.mattdyson.org/projects/blinkytape/BlinkyTapeV2.py)

### How do I add new light patterns? ###

1. Add the animation code in blinkycommands.py
2. Call that code either from an existing 'check' script (like checkforsnow.py or checkgmail.py), or create a new one

### Contribution guidelines ###

* Please contribute!

### Who do I talk to? ###

* Contact roy.town@outlook.com

### License ###

MIT
