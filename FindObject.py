from myro import *
from ObjectBlobFunction import determineDirection

#init("/dev/tty.IPRE6-193914-DevB")

black =     makeColor( 0, 0, 0)
white =     makeColor(255, 255, 255)
blue =      makeColor( 0, 0, 255)
darkBlue =  makeColor( 0, 0, 100)
pink =      makeColor(255, 175, 175)
red =       makeColor(255, 0, 0)
darkRed =   makeColor(100, 0, 0)
green =     makeColor( 0, 255, 0)
darkGreen = makeColor(0, 100, 0)
gray =      makeColor(128, 128, 128)
darkGray =  makeColor( 64, 64, 64)
lightGray = makeColor(192, 192, 192)
yellow =    makeColor(255, 255, 0)
magenta =   makeColor(255, 0, 255)
cyan =      makeColor( 0, 255, 255)
purple =    makeColor(127, 0, 255)
orange =    makeColor(225,100, 0)

setIRPower = 130

def findColour(colour):

    direction = determineDirection(colour)

    while getObstacle("Center") <= 1100 and not direction == "NONE":

        direction = determineDirection(colour)

        if (direction == "NONE"):
            turnRight(.3,.3)
        elif (direction == "LEFT"):
            turnLeft(.3,.3)
        elif (direction == "RIGHT"):
            turnRight(.3,.3)
        elif (direction == "CENTER"):
            forward(1,1)
