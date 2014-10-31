setIRPower(130)

rightPower = 0
leftPower = 0

while(True):

	#Using Obstacle Sensors

	#rightPower = leftPower = 1 - (getObstacle("center") / 550)
	#motors(leftPower,rightPower)


	#Using IR Sensors
	#rightPower = getIR(1) / 2
	#leftPower = getIR(0) / 2
	#motors(rightPower, leftPower)



	# #another test

	# left = getIR("left")
	# leftPower = 0
	# motors(leftPower, rightPower)
	# right = getIR("right")
	# rightPower = 0
	# motors(leftPower, rightPower)
	# leftPower = left / 2
	# motors(leftPower, rightPower)
	# rightPower = right / 2
	# leftPower=getIR("right")
	# rightPower=getIR("left")
	# motors(-leftPower, -rightPower)
	right=getObstacle("center")
	if(right >= 600):
		rightPower = -0.5
	else:
		rightPower = 0.5
	motors(leftPower, rightPower)
	left=getObstacle("left")
	if(left >= 600):
		leftPower = -0.5
	else:
		leftPower = 0.5
	motors(leftPower, rightPower)
	print "left: ", left
	print "rite: ", right