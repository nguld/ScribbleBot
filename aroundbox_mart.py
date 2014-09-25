direction		= 1 #Set to -1 if robot moves backward

highSpeed		= 1
lowSpeed		= 0.5
turnSpeed		= 0.5
checkInterval		= 0.3
moveMultiplierAfterTurn	= 5

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
	turnTime += checkInterval

	if (getIR(left) == something or getIR(right) == something):
		doAgain = 1
	elif (lastTime = 0):
		doAgain = 1
		lastTime = 1
	else
		doAgain = 0

# Use time to move around
forward (lowSpeed*direction, moveMultiplierAfterTurn*turnTime)
turnLeft (turnSpeed, turnTime)
forward (lowSpeed*direction, 2*moveMultiplierAfterTurn*turnTime)
turnLeft (turnSpeed, turnTime)
forward (lowSpeed*direction, moveMultiplierAfterTurn*turnTime)
turnRight (turnSpeed, turnTime)

# Move until it comes close to another object
while (getIR(left) == nothing and getIR(right) == nothing):
	forward (highSpeed*direction, checkInterval)
