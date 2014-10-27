from FindObject import *
import urllib2
from Queue import *
import threading
import thread

queue = Queue()

class updateQueueThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        updateQueue()
        print "Exiting " + self.name

class runQueueThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        runQueue()
        print "Exiting " + self.name

clearQueue = 0;

def updateQueue():
    while True:
        #print "Update Queue"
        data = urllib2.urlopen("http://www.noahguld.com/scribblerBot/output/commands.txt")

        for line in data:
            print line
            if line == "stop()\n":
                print "STOP"
                #runQueue.stop()
                clearQueue = 1;
                while queue.empty() == False:
                    queue.get()
                clearQueue = 0;
                #runQueue.start()
            else:
                queue.put(line)
            urllib2.urlopen("http://www.noahguld.com/scribblerBot/clearline.php")

def runQueue():
    while True:
        #print "Run Queue"
        while queue.empty() == False:
            if clearQueue != 1:
                exec queue.get()




#threads[0] = thread.start_new_thread(updateQueue, ())
#threads[1] = thread.start_new_thread(runQueue, ())
#thread1 = StoppableThread(thread.start_new_thread(runQueue, ()))
#thread.start_new_thread(updateQueue, ())
#thread.start_new_thread(runQueue, ())
updateThread = updateQueueThread(1, "updateThread")
runThread = runQueueThread(2, "runThread")

updateThread.start()
runThread.start()
