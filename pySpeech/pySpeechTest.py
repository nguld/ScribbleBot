import speech

def response(phrase, listener):
    speech.say("You said %s" % phrase)
    if phrase == "turn off":
        listener.stoplistening()

listener = speech.listenforanything(response)

# Your program can do whatever it wants now, and when a spoken phrase is heard,
# response() will be called on a separate thread.
import time
while listener.islistening():
    time.sleep(1)
    print "Still waiting..."