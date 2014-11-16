from __future__ import division
from myro import *
import subprocess
import os
import signal
import sys

def isPhoneConnected():
	a = subprocess.Popen(["redis-cli", "--csv", "-h", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "-p", "16825", "-a", "GiJiJuKaMaNoRo", "PUBSUB", "NUMSUB", "scribblerPhoneCommands"], shell=False, stdout=subprocess.PIPE)
	retval = a.stdout.readline()
	a.stdout.close()

	if ('"scribblerPhoneCommands","1"' in retval):
		return True
	else:
		print retval
		return False

def seesObstacle(tolerance):
	if (tolerance == "high"):
		tolerance = 100
	else:
		tolerance = 1000

	return getObstacle("left") >= tolerance or getObstacle("center") >= tolerance or getObstacle("right") >= tolerance

def moveStraightFallback():
	maxTime = 3
	startTime = time.time()
	move(-1, 0)
	while (seesObstacle("low") == False and time.time()-startTime < maxTime):
		pass
	stop()

def turnRightByDegreesFallback(degrees):
	rightTurnTime = 1.4
	turnTime = (degrees / 90.0) * rightTurnTime
	turnRight(0.5, turnTime)

def turnLeftByDegreesFallback(degrees):
	leftTurnTime = 1.4
	turnTime = (degrees / 90.0) * leftTurnTime
	turnLeft(0.5, turnTime)

def turnRightByDegrees(degrees, speed = 0.3):
	turnByDegrees(degrees, speed, -1)
def turnLeftByDegrees(degrees, speed = 0.3):
	turnByDegrees(degrees, speed, 1)

def turnByDegrees(degrees, speed, direction = 1):
	if not isPhoneConnected():
		if direction == 1:
			turnLeftByDegreesFallback(degrees)
		else:
			turnRightByDegreesFallback(degrees)
		return
	
	a = subprocess.Popen(["java", "-jar", "JavaRedis.jar", "pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com", "10592", "GiJiJuKaMaNoRo", "scribblerCompass"], shell=False, stdout=subprocess.PIPE)

	initialCompass = -1
	finalCompass = -1
	upperBound = -1
	lowerBound = -1

	while (True):
		phoneCompass = int(float(a.stdout.readline()))
		if (phoneCompass != ""):
			if (initialCompass == -1):
				initialCompass = phoneCompass
				finalCompass = (phoneCompass-direction*degrees)%360
			else:
				if (initialCompass == phoneCompass):
					break
				else:
					initialCompass = phoneCompass
					finalCompass = (phoneCompass-direction*degrees)%360

	print "Starts At: ", initialCompass				
	a.stdout.close()

	if (direction == 1):
		turnLeftByDegreesFallback(degrees)
	else:
		turnRightByDegreesFallback(degrees)
	
	a = subprocess.Popen(["java", "-jar", "JavaRedis.jar", "pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com", "10592", "GiJiJuKaMaNoRo", "scribblerCompass"], shell=False, stdout=subprocess.PIPE)

	iteration = 0
	finalCheck = False
	while (True):
		phoneCompass = int(float(a.stdout.readline()))
		if (phoneCompass != ""):
			print "Current: ", phoneCompass

			difference = phoneCompass - finalCompass
			difference2 = (phoneCompass+360) - finalCompass
			difference3 = (phoneCompass-360) - finalCompass
			if (abs(difference2) < abs(difference)): difference = difference2
			if (abs(difference3) < abs(difference)): difference = difference3

			print "Difference: ", difference
			
			if (abs(difference) == 0):
				if (finalCheck): break
				else: finalCheck = True
			elif (difference < 0):
				move(0, -0.05)
			else:
				move(0, 0.05)

			if iteration > 100:
				break
			iteration += 1

	a.stdout.close()

	stop()


#def turnByDegrees(degrees, speed, direction = 1):
#	if not isPhoneConnected():
#		if direction == 1:
#			turnLeftByDegreesFallback(degrees)
#		else:
#			turnRightByDegreesFallback(degrees)
#		return
#	
#	move(0,direction*speed)
#
#	a = subprocess.Popen(["/home/martvanburen/Desktop/jdk1.8.0_25/bin/java", "-jar", "Movement Commands/JavaRedis.jar", "pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com", "10592", "GiJiJuKaMaNoRo", "scribblerCompass"], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid)
#
#	iteration = 0
#	initialCompass = -1
#	while (True):
#		phoneCompass = int(float(a.stdout.readline()))
#		if (phoneCompass != ""):
#			if (iteration == 0):
#				initialCompass = phoneCompass
#
#			upperBound = (initialCompass+(degrees+5))
#			lowerBound = (initialCompass+(degrees-10))
#			print "Lower: ", lowerBound
#			print "Upper: ", upperBound
#			print "Current: ", phoneCompass
#			if ((phoneCompass > lowerBound and phoneCompass < upperBound) or
#				(phoneCompass+360 > lowerBound and phoneCompass+360 < upperBound)):
#				stop()
#				break
#			iteration += 1
#	
#	os.killpg(a.pid, signal.SIGTERM)


from myro import *
init("com3")
turnRightByDegrees(90)