from Parser import parse
from speakCustom import *
from Sounds import *
from FindObject import *
from GetColour import *
from Queue import *
from Movements import *
from Myo import *
import threading
import subprocess
import sys

queue = Queue()

class newThread (threading.Thread):
    def __init__(self, function):
        threading.Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()

# def updateCommand():
#     a = subprocess.Popen(["java", "-jar", "JavaRedis.jar", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "16825", "GiJiJuKaMaNoRo", "scribblerCommands"], shell=False, stdout=subprocess.PIPE)
#     while (True):
#         sys.stdout.write(a.stdout.readline())

# def updateMyoPoseData():
#     b = subprocess.Popen(["java", "-jar", "javaredis.jar", "pub-redis-10683.us-east-1-2.5.ec2.garantiadata.com ", "10683", "GiJiJuKaMaNoRo", "scribblerMyoPoses"], shell=False, stdout=subprocess.PIPE)
#     while (True):
#         pyoPose = c.stdout.readline()
#         print pyoPose

# def updateMyoSensorData():
#     c = subprocess.Popen(["java", "-jar", "javaredis.jar", "pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com", "10592", "GiJiJuKaMaNoRo", "scribblerMyoSensors"], shell=False, stdout=subprocess.PIPE)
#     while (True):
#         myoSensors = d.stdout.readline()
#         print myoSensors

def updateQueue():
    a = subprocess.Popen(["java", "-jar", "JavaRedis.jar", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "16825", "GiJiJuKaMaNoRo", "scribblerCommands"], shell=False, stdout=subprocess.PIPE)
    while True:
        text = a.stdout.readline()
        if(text!=""):
            parsed = parse(text)
            if parsed == "stopCurrent()":
                try:
                    stop()
                except:
                    pass
                init("com3")
                aNewThread = newThread(runQueue)
                aNewThread.start()
            elif  parsed == "stopAll()":
                try:
                    stop()
                except:
                    pass
                init("com3")
                while queue.empty() == False:
                    queue.get()
                aNewThread = newThread(runQueue)
                aNewThread.start()
            else:
                queue.put(parsed)

def runQueue():
    while True:
        while queue.empty() == False:
            exec queue.get()


# compassThread = newThread (updateCompass)
# commandThread = newThread (updateCommand)
# poseThread = newThread(3, "poseThread")
# sensorsThread = newThread(4, "sensorsThread")
updateThread = newThread(updateQueue)
runThread = newThread(runQueue)

# compassThread.start()
# commandThread.start()
# poseThread.start()
# sensorsThread.start()
updateThread.start()
runThread.start()