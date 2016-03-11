#!/bin/sh

kill $(ps aux | grep 'python queuemanager.py' | awk '{ print $2 }')
kill $(ps aux | grep 'python commandhttpserver.py' | awk '{ print $2 }')
kill $(ps aux | grep 'python checkgmail.py' | awk '{ print $2 }')
kill $(ps aux | grep 'python checkforsnow.py' | awk '{ print $2 }')

python queuemanager.py &
python commandhttpserver.py &
python checkgmail.py &
python checkforsnow.py &
