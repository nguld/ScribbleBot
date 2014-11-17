from __future__ import division
from myro import *
import redis
import subprocess
import os
import signal
import sys

def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

def getMyoData(channel = "scribblerMyoSensors"):
	return subprocess.Popen(["/home/martvanburen/Desktop/jdk1.8.0_25/bin/java", "-jar", "JavaRedis.jar", "pub-redis-10683.us-east-1-2.5.ec2.garantiadata.com", "10683", "GiJiJuKaMaNoRo", channel], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid)

def killSubProcess(proc):
	os.killpg(proc.pid, signal.SIGTERM)

def redisPublish(message, channel = "scribblerPhoneCommands"):
	a = subprocess.Popen(["redis-cli", "--csv", "-h", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "-p", "16825", "-a", "GiJiJuKaMaNoRo", "PUBLISH", channel, message], shell=False, stdout=subprocess.PIPE)

def minimalDifference(a, b):
	dif = a - b
	dif2 = (a+18) - b
	dif3 = (a-18) - b
	if (abs(dif2) < abs(dif)): dif = dif2
	if (abs(dif3) < abs(dif)): dif = dif3
	return dif

def myoDrive():
	a = getMyoData()
	b = getMyoData("scribblerMyoPoses")

	myoCalibrationPoint = ""

	while (True):
		myoPose = b.stdout.readline()
		myoSensor = a.stdout.readline()
		if (myoPose != "" and myoSensor != ""):
			if ("fingersSpread" in myoPose):
				myoCalibrationPoint = myoSensor
				break
			else:
				print "Nope: ", myoPose

	print "Calibration Point: ", myoCalibrationPoint			
	killSubProcess(a)

	redisPublish('speak("Lets Roll")')
	
	myoCalibrationPoint = find_between(myoCalibrationPoint, '[', ']').split(',')
	
	calRoll = int(float(myoCalibrationPoint[0]))
	calPitch = int(float(myoCalibrationPoint[1]))
	calYaw = int(float(myoCalibrationPoint[2]))

	a = getMyoData()

	iteration = 0
	while (True):
		myoSensor = a.stdout.readline()
		if (myoSensor != ""):
			myoSensor = find_between(myoSensor, '[', ']').split(',')
			curRoll = int(float(myoSensor[0]))
			curPitch = int(float(myoSensor[1]))
			curYaw = int(float(myoSensor[2]))

			difRoll = minimalDifference(curRoll, calRoll)
			difPitch = minimalDifference(curPitch, calPitch)
			difYaw = minimalDifference(curYaw, calYaw)

			print "difRoll: ", difRoll
			print "difPitch: ", difPitch
			print "difYaw: ", difYaw

			rotationalComponent = 0.6*(difRoll/3)
			movementComponent = (difPitch/5)
			
			move(movementComponent, -rotationalComponent)
			
			if (abs(difYaw) > 8):
				break
			iteration += 1
	
	stop()
