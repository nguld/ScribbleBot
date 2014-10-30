import time
import sys

IRPower1 = 128
IRPower2 = 125
highSpeed = 0.8
lowSpeed = 0.5
waitTime = 0.3
angleCorrectionTurnTime = 0.1

# Trial and error, not really in cm or anything (seconds if anything)
#distanceFromBox = 4
distanceFromBox = 0.5
# Time, in seconds, to move if it still sees object after turning
trialAndErrorMoveIncrements = 0.6

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
def rightTurnRight(speed, turns = 0):
	if (speed == "slow"):
		# NOTE Calculating horizontalClearanceTime relies on these value
		rightTurnTime = 0.205
		rightTurnRepeat = 6
	else:
		rightTurnTime = 0.4
		rightTurnRepeat = 3

	if (turns != 0): rightTurnRepeat = turns
	
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
		# Return turns until it sees no object
		j = 1
		for i in range(rightTurnRepeat):
			turnRight(lowSpeed, rightTurnTime)
			wait(waitTime)
			if seesObstacle("high"):
				#if (j == 3): return 3
				return j
				break
			j += 1
		
		return 0

# If it sees an object, it turns 90 degrees left and returns time until it no longer saw object
# Otherwise it turns 90 degrees left and returns whether it now sees an obstacle
# Accepts either speed slow (accurate timeUntilNoObject) or fast
def rightTurnLeft(speed, turns = 0):
	if (speed == "slow"):
		rightTurnTime = 0.205
		rightTurnRepeat = 6
	else:
		rightTurnTime = 0.4
		rightTurnRepeat = 3

	if (turns != 0): rightTurnRepeat = turns

	if (seesObstacle("high") == True):
		timeUntilNoObject = rightTurnTime
		
		for i in range(rightTurnRepeat):
			turnLeft(lowSpeed, rightTurnTime)
			wait(waitTime)
			if (seesObstacle("high") == True):
				timeUntilNoObject += rightTurnTime

		return timeUntilNoObject
	else:
		# Return turns until it sees no object
		j = 1
		for i in range(rightTurnRepeat):
			turnLeft(lowSpeed, rightTurnTime)
			wait(waitTime)
			if seesObstacle("high"):
				#if (j == 3): return 3
				return j
				break
			j += 1
		
		return 0

# Turns left a little, checks to see if there is an obstacle, and turns back (returning presence of obstacle)
def clearanceCheckLeft():
	turnTime = 0.205
	obstacleDetected = False

	turnLeft(lowSpeed, turnTime)
	wait(waitTime)

	if seesObstacle("high"):
		obstacleDetected = True

	if (obstacleDetected == False):
		turnLeft(lowSpeed, turnTime)
		wait(waitTime)
	
		if seesObstacle("high"):
			obstacleDetected = True
	
		turnRight(lowSpeed, turnTime)
		wait(waitTime)

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

# Checks for the angle of the box, and returns how much it rotated to be perpendicular to the box
def checkAngle():
	totalTimesTurningRight = 0
	totalTimesTurningLeft = 0

	toleranceRight = -100
	toleranceLeft = 120

	# Try turning left
	while True:
		curProximity = getObstacle('center')
		turnLeft(lowSpeed, angleCorrectionTurnTime)
		totalTimesTurningLeft += 1
		wait(waitTime)
		newProximity = getObstacle('center')
		#turnLeft(lowSpeed, angleCorrectionTurnTime)
		#totalTimesTurningLeft += 1
		#wait(waitTime)
		#newProximity2 = getObstacle('center')

		printInfo("Before: " + str(curProximity) + " & After 1: " + str(newProximity)) # + " & After 2: " + str(newProximity2))

		if (curProximity - newProximity > -toleranceLeft): # and curProximity - newProximity2 > -toleranceLeft):
			# Object is further from pependicular
			for i in range(2):
				turnRight(lowSpeed, angleCorrectionTurnTime)
				totalTimesTurningLeft -= 1
				wait(waitTime)
			break;
	# Try turning right
	while True:
		curProximity = getObstacle('center')
		turnRight(lowSpeed, angleCorrectionTurnTime)
		totalTimesTurningRight += 1
		wait(waitTime)
		newProximity = getObstacle('center')
		#turnRight(lowSpeed, angleCorrectionTurnTime)
		#totalTimesTurningRight += 1
		#wait(waitTime)
		#newProximity2 = getObstacle('center')

		printInfo("Before: " + str(curProximity) + " & After 1: " + str(newProximity)) # + " & After 2: " + str(newProximity2))

		if (curProximity - newProximity > -toleranceRight): # and curProximity - newProximity2 > -toleranceRight):
			# Object is further from pependicular
			for i in range(2):
				turnLeft(lowSpeed, angleCorrectionTurnTime)
				totalTimesTurningRight -= 1
				wait(waitTime)
			break;

	return totalTimesTurningRight - totalTimesTurningLeft

setIRPower(IRPower1)

# Move until it sees obstacle
printKeyStep("Moving...")
move(highSpeed, 0)
while (seesObstacle("low") == False):
	pass
stop()
wait(waitTime)
printKeyStep("Object spotted")

setIRPower(IRPower2)

# Account for initial box angle
angleCorrectionTime = checkAngle()
print "Times until perpendicular: ", angleCorrectionTime

# Calculate rotating time until it does not see object
printKeyStep("Turning right to get to edge of box")
timeUntilNoObject = rightTurnRight("slow")
if (timeUntilNoObject == True or timeUntilNoObject == False): timeUntilNoObject = "NO OBJECT IN FIRST PLACE"
print "Time until no object: ", timeUntilNoObject

# Calculate approximate time to move and do it
angle = (timeUntilNoObject / (0.4 * 3)) * math.radians(90) # Assume radians
horizontalBoxClearTime = distanceFromBox * math.tan(angle)
#horizontalBoxClearTime = trialAndErrorMoveIncrements
# Sanity checks
if horizontalBoxClearTime < 0.6: horizontalBoxClearTime = 0.6
if horizontalBoxClearTime > 4: horizontalBoxClearTime = 4
print "Calculated horizontal clearance time: ", horizontalBoxClearTime
moveForward(highSpeed, horizontalBoxClearTime)
wait(waitTime)

# Turn left again and repeat if it still sees object
printKeyStep("Turning left to get to side of box")
turnsUntilObject = rightTurnLeft("fast")
print "At start: ", turnsUntilObject
stillSeesObject = (turnsUntilObject != 0)
# Rotate a little to the left and see if there is still nothing
if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
while (stillSeesObject == True):
	if (stillSeesObject): print "Still sees object after left turn, trying again"
	wait(waitTime)
	rightTurnRight("fast", turnsUntilObject)
	moveForward(highSpeed, trialAndErrorMoveIncrements)
	wait(waitTime)
	horizontalBoxClearTime += trialAndErrorMoveIncrements
	print "Before: ", turnsUntilObject
	turnsUntilObject = rightTurnLeft("fast")
	print "After: ", turnsUntilObject
	stillSeesObject = (turnsUntilObject != 0)
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
	turnsUntilObject  = rightTurnLeft("fast")
	stillSeesObject = (turnsUntilObject != 0)
	print turnsUntilObject
	# Rotate a little to the left and see if there is still nothing
	if (stillSeesObject == False): stillSeesObject = clearanceCheckLeft()
	while (stillSeesObject == True):
		if (stillSeesObject): print "Still sees object after left turn (trying to get to back of box), trying again"
		wait(waitTime)
		rightTurnRight("fast", turnsUntilObject)
		moveForward(highSpeed, trialAndErrorMoveIncrements)
		wait(waitTime)
		turnsUntilObject = rightTurnLeft("fast")
		stillSeesObject = (turnsUntilObject != 0)
		print turnsUntilObject
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
