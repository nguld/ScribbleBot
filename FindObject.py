from myro import *
from ObjectBlobFunction import determineDirection

#init("/dev/tty.IPRE6-193914-DevB")

#black =     makeColor( 0, 0, 0)
#white =     makeColor(255, 255, 255)
#blue =      makeColor( 0, 0, 255)
#darkBlue =  makeColor( 0, 0, 100)
#pink =      makeColor(255, 175, 175)
#red =       makeColor(255, 0, 0)
#darkRed =   makeColor(100, 0, 0)
#green =     makeColor( 0, 255, 0)
#darkGreen = makeColor(0, 100, 0)
#gray =      makeColor(128, 128, 128)
#darkGrey =  makeColor( 64, 64, 64)
#lightGrey = makeColor(192, 192, 192)
#yellow =    makeColor(255, 255, 0)
#magenta =   makeColor(255, 0, 255)
#purple =    makeColor(127, 0, 255)
#orange =    makeColor(225,100, 0)

colourKey = {'black': makeColor( 0, 0, 0),
            'white': makeColor(255, 255, 255),
            'blue': makeColor( 0, 0, 255),
            'dark blue': makeColor( 0, 0, 100),
            'pink': makeColor(255, 175, 175),
            'red': makeColor(255, 0, 0),
            'dark red': makeColor(100, 0, 0),
            'grey': makeColor(128, 128, 128),
            'dark grey': makeColor( 64, 64, 64),
            'light grey': makeColor(192, 192, 192),
            'yellow': makeColor(255, 255, 0),
            'magenta': makeColor(255, 0, 255),
            'cyan': makeColor( 0, 255, 255),
            'purple': makeColor(127, 0, 255),
            'orange': makeColor(225,100, 0),
            'green': makeColor( 0, 255, 0),
            'dark green': makeColor(0, 100, 0)}

setIRPower = 130

def findColour(key):

    colour = colourKey[key]

    leftMotor = 1
    rightMotor = 1
    lastSeenPos = "NONE"
    counter = 0;
    while True:#getObstacle("Center") <= 1100 and direction != "NONE":
        counter += 1
        direction = determineDirection(colour, counter)
        beep(.1)

        if (direction == "FARLEFT"):
            lastSeenPos = "LEFT"
            rightMotor = .7
            leftMotor = .3
        if (direction=="MIDLEFT"):
            lastSeenPos = "LEFT"
            rightMotor = .7
            leftMotor  = .5
        if (direction=="LEFTCENTER"):
            lastSeenPos = "LEFT"
            rightMotor = .7
            leftMotor  = .6
        if (direction=="RIGHTCENTER"):
            lastSeenPos = "RIGHT"
            rightMotor = .6
            leftMotor  = .7
        if (direction=="MIDRIGHT"):
            lastSeenPos = "RIGHT"
            rightMotor = .5
            leftMotor  = .7
        if (direction=="FARRIGHT"):
            lastSeenPos = "RIGHT"
            rightMotor = .3
            leftMotor  = .7
        if (direction=="NONE"):
            if lastSeenPos == "RIGHT":
                rightMotor = -.2 #Turn Right
                leftMotor = .2
            else:
                rightMotor = .2 #Turn Left
                leftMotor = -.2

            #lastSeenPos = "NONE"
        if (direction=="FAILED"):
            #lastSeenPos = "FAILED"
            rightMotor = 0
            leftMotor = 0
        #print "UNKNOWN 'direction'"
                
        motors(leftMotor,rightMotor)

#findColour('black');
#while True:
 #   kc = input()
  #  findKColour(kc)
