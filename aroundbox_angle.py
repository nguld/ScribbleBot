import time
import sys

IRPower = 128
highSpeed = 1
lowSpeed = 0.5
waitTime = 0.3
angleCorrectionTurnTime = 0.1

# Trial and error, not really in cm or anything (seconds if anything)
#distanceFromBox = 4
distanceFromBox = 0.5
# Time, in seconds, to move if it still sees object after turning
trialAndErrorMoveIncrements = 0.8

class color:
	PURPLE		= '\033[95m'
	CYAN		= '\033[96m'
	DARKCYAN	= '\033[36m'
	BLUE		= '\033[94m'
	GREEN		= '\033[92m'
	YELLOW		= '\033[93m'
	RED		= '\033[91m'
	BOLD		= '\033[1m'
	UNDERLINE	= '\033[4m'
	END		= '\033[0m'

# Takes either "high" or "low" as tolerance and returns if it sees an object in front of it as true or false
def seesObstacle(tolerance):
	if (tolerance == "high"):
		tolerance = 200
	else:
		tolerance = 1100

	return getObstacle("left") >= tolerance or getObstacle("center") >= tolerance or getObstacle("right") >= tolerance

# Returns current clock time in seconds
def getTime():
	return time.time()

# Print key steps in bold green
def printKeyStep(text):
	print color.BOLD + color.GREEN + text + color.END + color.END
# Print info in blue
def printInfo(text):
	print color.BLUE + text + color.END
# Print error in red
def printError(text):
	print color.RED + text + color.END

# If it sees an object, it turns 90 degrees right and returns time until it no longer saw object
# Otherwise it turns 90 degrees and returns whether it now sees an obstacle
# Accepts either speed slow (accurate timeUntilNoObject) or fast
def rightTurnRight(speed):
	if (speed == "slow"):
		# NOTE Calculating horizontalClearanceTime relies on these value
		rightTurnTime = 0.205
		rightTurnRepeat = 6
	else:
		rightTurnTime = 0.4
		rightTurnRepeat = 3
	
	if (seesObstacle("high") == True):
		timeUntilNoObject = rightTurnTime
		
		for i in range(rightTurnRepeat):
			turnRight(lowSpeed, rightTurnTime)
			wait(waitTime)
			printInfo("Obstacle Sensor: " + str(getObstacle("center")))
			if (seesObstacle("high") == True):
				printInfo("Adding " + str(rightTurnTime) + "s")
				timeUntilNoObject += rightTurnTime

		return timeUntilNoObject
	else:
		for i in range(rightTurnRepeat):
			turnRight(lowSpeed, rightTurnTime)
			wait(waitTime)

		return seesObstacle("high")

# If it sees an object, it turns 90 degrees left and returns time until it no longer saw object
# Otherwise it turns 90 degrees left and returns whether it now sees an obstacle
# Accepts either speed slow (accurate timeUntilNoObject) or fast
def rightTurnLeft(speed):
	if (speed == "slow"):
		rightTurnTime = 0.205
		rightTurnRepeat = 6
	else:
		rightTurnTime = 0.4
		rightTurnRepeat = 3

	if (seesObstacle("high") == True):
		timeUntilNoObject = rightTurnTime
		
		for i in range(rightTurnRepeat):
			turnLeft(lowSpeed, rightTurnTime)
			wait(waitTime)
			if (seesObstacle("high") == True):
				timeUntilNoObject += rightTurnTime

		return timeUntilNoObject
	else:
		for i in range(rightTurnRepeat):
			turnLeft(lowSpeed, rightTurnTime)
			wait(waitTime)

		return seesObstacle("high")

# Turns left a little, checks to see if there is an obstacle, and turns back (returning presence of obstacle)
def clearanceCheckLeft():
	turnTime = 0.4
	obstacleDetected = False

	turnLeft(lowSpeed, turnTime)
	wait(waitTime)

	obstacleDetected = seesObstacle("high")

	turnRight(lowSpeed, turnTime)
	wait(waitTime)
	
	return obstacleDetected

# Move only if there is nothing in the way AT THE START
def moveForward(speed, time):
	if (seesObstacle("high") == False):
		forward(speed, time)
	else: 
		printError("Unexpected object")
		sys.exit(0)

# Move only if there is nothing in the way
# Returns travel time
def moveForwardCarefully(speed, time, errorOnObstacle):
	startTime = getTime()
	move(speed, 0)
	while (seesObstacle("low") == False and getTime()-startTime < time):
		pass
	stop()
	wait(waitTime)
	
	elapsedTime = getTime() - startTime
	if (time - elapsedTime > 0.1 and errorOnObstacle == True):
		# Unexpected obstacle encountered
		printError("Unexpected object")
		sys.exit(0)

	return elapsedTime

# Returns average obstacle sensor values
def getObstacleAverage():
	#getObstacle1 = getObstacle('center')
	#wait(waitTime)
	#getObstacle2 = getObstacle('center')
	#return (getObstacle2 + getObstacle1)/2
	return getObstacle('center')

# Checks for the angle of the box, and returns how much it rotated to be perpendicular to the box
def checkAngle():
	totalTimesTurningRight = 0
	totalTimesTurningLeft = 0

	# Try turning right
	while True:
		curProximity = getObstacleAverage()
		turnRight(lowSpeed, angleCorrectionTurnTime)
		totalTimesTurningRight += 1
		wait(waitTime)
		newProximity = getObstacleAverage()

		printInfo("Before: " + str(curProximity) + " & After: " + str(newProximity))

		if (newProximity < curProximity):
			# Object is further from pependicular
			turnLeft(lowSpeed, angleCorrectionTurnTime)
			totalTimesTurningRight -= 1
			wait(waitTime)
			turnLeft(lowSpeed, angleCorrectionTurnTime)
			totalTimesTurningRight -= 1
			wait(waitTime)
			break;
	# Try turning left
	while True:
		curProximity = getObstacleAverage()
		turnLeft(lowSpeed, angleCorrectionTurnTime)
		totalTimesTurningLeft += 1
		wait(waitTime)
		newProximity = getObstacleAverage()

		printInfo("Before: " + str(curProximity) + " & After: " + str(newProximity))

		if (newProximity < curProximity):
			# Object is further from pependicular
			turnRight(lowSpeed, angleCorrectionTurnTime)
			totalTimesTurningLeft -= 1
			wait(waitTime)
			turnRight(lowSpeed, angleCorrectionTurnTime)
			totalTimesTurningLeft -= 1
			wait(waitTime)
			break;

	return totalTimesTurningRight - totalTimesTurningLeft

setIRPower(IRPower)
	
# Move until it sees obstacle
printKeyStep("Moving...")
move(highSpeed, 0)
while (seesObstacle("low") == False):
	pass
stop()
wait(waitTime)
printKeyStep("Object spotted")

# Account for initial box angle
angleCorrectionTime = checkAngle()
print "Time until perpendicular: ", angleCorrectionTime

# Calculate rotating time until it does not see object
printKeyStep("Turning right to get to edge of box")
timeUntilNoObject = rightTurnRight("slow")
if (timeUntilNoObject == True or timeUntilNoObject == False): timeUntilNoObject = "NO OBJECT IN FIRST PLACE"
print "Time until no object: ", timeUntilNoObject

# Calculate approximate time to move and do it
angle = (timeUntilNoObject / (0.4 * 3)) * math.radians(90) # Assume radians
horizontalBoxClearTime = distanceFromBox * math.tan(angle)
# Sanity checks
if horizontalBoxClearTime < 0.8: horizontalBoxClearTime = 0.8
if horizontalBoxClearTime > 4: horizontalBoxClearTime = 4
print "Calculated horizontal clearance time: ", horizontalBoxClearTime
moveForward(highSpeed, horizontalBoxClearTime)
wait(waitTime)

# Turn left again and repeat if it still sees object
printKeyStep("Turning left to get to side of box")
stillSeesObject = rightTurnLeft("fast")
# Rotate a little to the left and see if there is still nothing
if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
while (stillSeesObject == True):
	if (stillSeesObject): print "Still sees object after left turn, trying again"
	wait(waitTime)
	rightTurnRight("fast")
	moveForward(highSpeed, trialAndErrorMoveIncrements)
	wait(waitTime)
	horizontalBoxClearTime += trialAndErrorMoveIncrements
	stillSeesObject = rightTurnLeft("fast")
	if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
	print "Recalculated horizontal clearance time: ", horizontalBoxClearTime

# As an estimate, assume verticalBoxClearTime = horizontalBoxClearTime/2
horizontalBoxClearTime -= 0.3 # It's usually a bit long
verticalBoxClearTime = horizontalBoxClearTime/2
if (verticalBoxClearTime < 2): verticalBoxClearTime = 2

while (horizontalBoxClearTime > 0.1): #horizantalBoxClearTime is decreased as the box returns to its starting line
	# Move until it is back where it started
	printKeyStep("Moving along side of box")
	moveForwardCarefully(highSpeed, verticalBoxClearTime, True)
	wait(waitTime)
	
	# Turn left again and repeat if it still sees object
	printKeyStep("Turning left to get to back of box")
	stillSeesObject = rightTurnLeft("fast")
	# Rotate a little to the left and see if there is still nothing
	if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
	while (stillSeesObject == True):
		if (stillSeesObject): print "Still sees object after left turn (trying to get to back of box), trying again"
		wait(waitTime)
		rightTurnRight("fast")
		moveForward(highSpeed, trialAndErrorMoveIncrements)
		wait(waitTime)
		verticalBoxClearTime += trialAndErrorMoveIncrements
		stillSeesObject = rightTurnLeft("fast")
		if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
	print "Calculated vertical clearance time: ", verticalBoxClearTime
	
	# Move back to start line
	printKeyStep("Moving back to starting line")
	travelTime = moveForwardCarefully(highSpeed, horizontalBoxClearTime, False)

	# Subtract time already traveled
	horizontalBoxClearTime -= travelTime
	print "Horizontal displacement left to go:", horizontalBoxClearTime
	if (horizontalBoxClearTime > 0.1):
		print "Couldn't get to starting line. Moving further and trying again."
	else:
		printKeyStep("Back at starting line!")
	verticalBoxClearTime = trialAndErrorMoveIncrements
	
	rightTurnRight("fast")

# Undo angle correction
if (angleCorrectionTime > 0):
	for i in range(0, angleCorrectionTime):
		turnLeft(lowSpeed, angleCorrectionTurnTime)
		wait(waitTime)
elif (angleCorrectionTime < 0):
	angleCorrectionTime *= -1
	for i in range(0, angleCorrectionTime):
		turnRight(lowSpeed, angleCorrectionTurnTime)
		wait(waitTime)

moveForwardCarefully(highSpeed, 2, False)
