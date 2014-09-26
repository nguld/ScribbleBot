direction		= -1 #Set to -1 if robot moves backward

highSpeed		= 1
lowSpeed		= 0.5
turnSpeed		= 0.5
checkInterval		= 0.4
moveMultiplierAfterTurn	= 6

turnTime = 0

# Constants
left = 0
right = 1
nothing = 1
something = 0

# Move until it comes close to an object
while (getIR(left) == nothing and getIR(right) == nothing):
	forward (highSpeed*direction, checkInterval)

# Count time until it no longer sees object
doAgain = 1
lastTime = 0
while (doAgain == 1):
	turnRight (turnSpeed, checkInterval)
	wait(0.5);
	turnTime += checkInterval

	if (getIR(left) == something or getIR(right) == something):
		doAgain = 1
	elif (lastTime == 0 or lastTime == 1):
		doAgain = 1
		lastTime += 1
	else:
		doAgain = 0

# Use time to move around
forward (lowSpeed*direction, moveMultiplierAfterTurn*turnTime)
turnLeft (turnSpeed, turnTime)
forward (lowSpeed*direction, 1.5*moveMultiplierAfterTurn*turnTime)
turnLeft (turnSpeed, turnTime)
forward (lowSpeed*direction, moveMultiplierAfterTurn*turnTime)
turnRight (turnSpeed, turnTime)

forward (highSpeed*direction, 1);

# Move until it comes close to another object
#while (getIR(left) == nothing and getIR(right) == nothing):
#	forward (highSpeed*direction, checkInterval)
