def right():
	turnRight(0.5, 0.435)
	wait(0.5)
	turnRight(0.5, 0.435)
	wait(0.5)
	turnRight(0.5, 0.435)
	wait(0.5)

def left():
	turnLeft(0.5, 0.435)
	wait(0.5)
	turnLeft(0.5, 0.435)
	wait(0.5)
	turnLeft(0.5, 0.435)
	wait(0.5)

def go():
	forward(0.5, 0.5)
	wait(0.5)

def isWall():
	if getObstacle("center") > 0:
		return True
	else:
		return False

setIRPower(124)

move(0.5,0)
while getObstacle("center") < 1100:
	pass

setIRPower(130)

stop()
wait(0.5)

count = 0

while isWall():
	count += 0.5
	right()
	go()
	left()

right()
go()
left()
left()

while not isWall():
	right()
	go()
	left()

while isWall():
	right()
	go()
	left()

right()
go()
left()

forward (0.5, count)
right()
forward(1,2)