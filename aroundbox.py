setForwardness("fluke-forward")
turnPower = .85
turnTime = .75
threshold = 1100
waitTime = .2

movePower = 1
moveTime = .5

def MovePastBoxSide():
	besideBox = True
	timeTraveled = 0
	while besideBox:
		turnLeft(turnPower, turnTime) # Turn to Box
		wait(waitTime)
		if not wall(threshold): # If don't see Box
			besideBox = False
			return timeTraveled
		turnRight(turnPower, turnTime) # Turn ortho to box
		forward(movePower, moveTime)
		timeTraveled += 1

def MoveAroundCorner():
	forward(movePower, moveTime)
	turnLeft(turnPower, turnTime)
	wait(waitTime)
	forward(movePower, moveTime)

while not wall(threshold): #returns True if getObstacle(1) is > threshold
	forward(movePower, moveTime)
# Stoped at Box
turnRight(turnPower, turnTime)
# Ortho to box

wait(waitTime)
totalTimeTraveled = MovePastBoxSide()
wait(waitTime)


# Past Bottom Side of Box
MoveAroundCorner()

wait(waitTime)
MovePastBoxSide()
wait(waitTime)

# Past Right Side of Box
MoveAroundCorner()

forward(movePower, totalTimeTraveled)

turnRight(turnPower, turnTime)
wait(waitTime)
forward(movePower, 5)