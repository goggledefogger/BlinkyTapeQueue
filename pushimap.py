import imaplib2, time
from threading import *
 
# This is the threading object that does all the waiting on 
# the event
class Idler(object):
    def __init__(self, conn,  newMailCallback):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
	self.newMailCallback = newMailCallback
 
    def start(self):
        self.thread.start()
 
    def stop(self):
        # This is a neat trick to make thread end. Took me a 
        # while to figure that one out!
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new 
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately, 
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()
 
    # The method that gets called when a new email arrives. 
    # Replace it with something better.
    def dosync(self):
        self.newMailCallback()
 
def startListening(username, password, newMailCallback):
	print "IMAP listening"
	# Had to do this stuff in a try-finally, since some testing 
	# went a little wrong.....
	try:
	    # Set the following two lines to your creds and server
	    M = imaplib2.IMAP4_SSL("imap.gmail.com")
	    M.login(username,password)
	    # We need to get out of the AUTH state, so we just select 
	    # the INBOX.
	    M.select("INBOX")
	    # Start the Idler thread
	    idler = Idler(M, newMailCallback)
	    idler.start()
	    # Because this is just an example, exit after 1 minute.
	    while True:
		# Let this sit in an infinite loop
		time.sleep(0.1)
	finally:
	    # Clean up.
	    idler.stop()
	    idler.join()
	    M.close()
	    # This is important!
	    M.logout()

def callbackStub():
	print "Callback stub"

if __name__ == "__main__":
	startListening("blinkytape@gmail.com", "helloroy", callbackStub)
