from __future__ import division
from myro import *
import redis
import subprocess
import os
import signal
import sys

def getCompassData(channel = "scribblerCompass"):
	return subprocess.Popen(["/home/martvanburen/Desktop/jdk1.8.0_25/bin/java", "-jar", "JavaRedis.jar", "pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com", "10592", "GiJiJuKaMaNoRo", channel], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid)

def killSubProcess(proc):
	os.killpg(proc.pid, signal.SIGTERM)

def isPhoneConnected():
	a = subprocess.Popen(["redis-cli", "--csv", "-h", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "-p", "16825", "-a", "GiJiJuKaMaNoRo", "PUBSUB", "NUMSUB", "scribblerPhoneCommands"], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid)
	retval = a.stdout.readline()
	killSubProcess(a)

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

def moveStraight(time = 3):
	maxTime = time
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

def turnRightByDegrees(degrees = 90, speed = 0.3):
    if (degrees > 180):
        times180 = int(degrees/180)
        degrees = int(degrees%180)
        for i in range(0, times180):
            turnByDegrees(180, speed, -1)
        turnByDegrees(degrees, speed, -1)
    else:
        turnByDegrees(degrees, speed, -1)
def turnLeftByDegrees(degrees = 90, speed = 0.3):
    if (degrees > 180):
        times180 = int(degrees/180)
        degrees = int(degrees%180)
        for i in range(0, times180):
            turnByDegrees(180, speed, 1)
        turnByDegrees(degrees, speed, 1)
    else:
        turnByDegrees(degrees, speed, 1)

def turnByDegrees(degrees, speed, direction = 1):
	if not isPhoneConnected():
		if direction == 1:
			turnLeftByDegreesFallback(degrees)
		else:
			turnRightByDegreesFallback(degrees)
		return
	
	a = getCompassData()

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
	killSubProcess(a)

	if (direction == 1):
		turnLeftByDegreesFallback(degrees)
	else:
		turnRightByDegreesFallback(degrees)
	
	a = getCompassData()

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

	killSubProcess(a)

	stop()

def turnToDegrees(degrees):
	if (not isPhoneConnected()):
		print "No phone connected"
		return
	
	a = getCompassData()

	initialCompass = -1
	finalCompass = degrees
	difference = -1

	while (True):
		phoneCompass = int(float(a.stdout.readline()))
		if (phoneCompass != ""):
			initialCompass = phoneCompass
			difference = phoneCompass - finalCompass
			difference2 = (phoneCompass+360) - finalCompass
			difference3 = (phoneCompass-360) - finalCompass
			if (abs(difference2) < abs(difference)): difference = difference2
			if (abs(difference3) < abs(difference)): difference = difference3
			break

	print "Starts At: ", initialCompass				
	killSubProcess(a)

	if (difference > 0):
		turnLeftByDegreesFallback(difference)
	else:
		turnRightByDegreesFallback(-difference)
	
	a = getCompassData()

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

	killSubProcess(a)

	stop()

def followCompass():
	if (not isPhoneConnected()):
		print "No phone connected"
		return
	
	a = getCompassData()
	b = getCompassData("scribblerCompassFollower")

	iteration = 0
	alignedIterations = 0
	while (True):
		phoneCompass = int(float(a.stdout.readline()))
		followingCompass = int(float(b.stdout.readline()))

		if (phoneCompass != "" and followingCompass != ""):
			print "Current: ", phoneCompass
			print "Following: ", followingCompass

			difference = phoneCompass - followingCompass
			difference2 = (phoneCompass+360) - followingCompass
			difference3 = (phoneCompass-360) - followingCompass
			if (abs(difference2) < abs(difference)): difference = difference2
			if (abs(difference3) < abs(difference)): difference = difference3

			print "Difference: ", difference
			
			if (abs(difference) < 10):
				alignedIterations += 1
			else:
				alignedIterations = 0

			catchupSpeed = -(1/54000)*(difference-180)**2+0.6
			#catchupSpeed = 0.00666667*difference - (0.0000185185)*(difference**2)

			catchupSpeed = abs(catchupSpeed)
			
			if (abs(difference) > 1):
				if (difference < 0):
					move(0, -catchupSpeed)
				else:
					move(0, catchupSpeed)
			else:
				stop()

			#if (alignedIterations > 100 or iteration > 500):
			#	break
			iteration += 1

	killSubProcess(a)

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
