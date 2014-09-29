 #Useful functions for myro

movePower = 1;
moveTime = 1;

turnPower = 1;
turnTime = .75;

 def degreeTurn(degrees): # Turn degrees amount


 def turn45(dir): # Turn 45 degrees in dir: (-)ve = left, (+)ve = right
 	turnP = .4
 	turnT = .4
 	if dir < 0:
 		turnLeft(turnP, turnT)
 		turnLeft(turnP, turnT)
 	else if dir > 0:
 		turnRight(turnP, turnT)
 		turnRight(turnP, turnT)
 	else:
 		print("Error in 'turn45': value in 'dir' not recognized")

 def turn90(dir): # Turn 90 degrees in dir: (-)ve = left, (+)ve = right
 	turnP = .4
 	turnT = .3
 	if dir < 0:
 		turnLeft(turnP, turnT)
 		turnLeft(turnP, turnT)
 		turnLeft(turnP, turnT)
 	else if dir > 0:
 		turnRight(turnP, turnT)
 		turnRight(turnP, turnT)
 		turnRight(turnP, turnT)
 	else:
 		print("Error in 'turn90': value in 'dir' not recognized")


 def travelStraight(distance): # Travel distance forward
 	if distance > 0:
 	
 	else if distance < 0:

 	else:
 		print("Error in 'travelStraight': value in 'distance' not recognized")
