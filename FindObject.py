from myro import *

#init("/dev/tty.IPRE6-193914-DevB")

from Sounds import *

###############################################################################
from math import *

####################################################
#                 Define Colours                   #
####################################################
black =     makeColor( 20, 20, 20)
white =     makeColor(235, 235, 235)
blue =      makeColor( 50, 50, 250)
darkBlue =  makeColor( 20, 20, 100)
pink =      makeColor(250, 175, 175)
red =       makeColor(250, 50, 50)
darkRed =   makeColor(100, 10, 10)
green =     makeColor( 50, 250, 50)
darkGreen = makeColor(20, 100, 20)
gray =      makeColor(128, 128, 128)
darkGray =  makeColor( 64, 64, 64)
lightGray = makeColor(192, 192, 192)
yellow =    makeColor(250, 250, 60)
magenta =   makeColor(250, 50, 250)
cyan =      makeColor( 50, 250, 250)
purple =    makeColor(127, 50, 250)
orange =    makeColor(225,100, 50)
green =     makeColor( 50, 250, 50)
darkGreen=  makeColor(20, 100, 20)
#####################################################



#####################################################
#                Image Processing                   #
#####################################################
#                                                   #
# 1) Change pixel colour based on colour tollerance #
#                                                   #
# 2) Determines what side of the picture the        #
#    majority of the pixels are only                #
#                                                   #
#####################################################
def determineDirection (colour, num):

    pic = takePicture() #Uncomment this for robot

    #path = os.path.dirname(os.path.realpath(__file__))
    #pic = makePicture(path + "/lucy.gif") #jpg or gif only

    RGBred, RGBgreen, RGBblue = getRGB(colour);

    h = getHeight(pic)
    w = getWidth(pic)

    # Variable for image analysis
    farLeftTotal = 0
    midLeftTotal = 0
    farRightTotal = 0
    midRightTotal = 0
    centerLeftTotal = 0
    centerRightTotal = 0
    totalArray = [farLeftTotal, midLeftTotal, centerLeftTotal, centerRightTotal, midRightTotal, farRightTotal]

    # How the screen is split up
    #fLS|mLS|cLS|cRS|mRS|fRS|
    #------------------------
    #   |   |   |   |   |   |
    #   |   |   |   |   |   |
    #   |   |   |   |   |   |
    #   |   |   |   |   |   |
    #   |   |   |   |   |   |
    #   |   |   |   |   |   |
    #------------------------

    numDivisions = 3
    distanceFromTollerance = 100
    
    for i in range(1, w, numDivisions):
        for j in range(1, h, numDivisions):
            pixel = getPixel(pic, i, j)
            r, g, b = getRGB(pixel)

            # FORMULA 1
            #distanceFrom = sqrt((r - RGBred)*(r - RGBred) + (g - RGBgreen)*(g - RGBgreen) + (b - RGBblue)*(b - RGBblue));
            distanceFrom = sqrt(pow(abs(r-RGBred),2) + pow(abs(g-RGBgreen),2) + pow(abs(b-RGBblue),2))
            
            if (distanceFrom < distanceFromTollerance):
                #############setRGB(pixel, (255,255,255))
                for index in range(0,6):
                    if i > (index) * (w/6): #Check if greater then lower
                        if i < (index+1) * (w/6):
                            totalArray[index] += 1
                            break
            ############else:
                ###########setRGB(pixel, (0,0,0))
            ########setPixel(pic, i/numDivisions, j/numDivisions, pixel)

    ########outputFile = "Processed" + str(num) + ".gif"
    #print outputFile
    #######savePicture(pic, outputFile)
    #show(pic)

    errorTollerance = 10

    #determine which total is largest to determine direction2
    indexOfLargest = -1
    largestNum = -1
    for index in range(0,6):
        if totalArray[index] > largestNum:
            largestNum = totalArray[index]
            indexOfLargest = index


    #Screen for error tollerance
    for i in range(0,5):
        if (abs(totalArray[i] - totalArray[i+1]) > errorTollerance):
            break
        if (i == 4):
            print "NONE"
            return "NONE"

    #print indexOfLargest
    if (indexOfLargest==0):
        print "FARLEFT"
        return "FARLEFT"
    if (indexOfLargest==1):
        print "MIDLEFT"
        return "MIDLEFT"
    if (indexOfLargest==2):
        print "LEFTCENTER"
        return "LEFTCENTER"
    if (indexOfLargest==3):
        print "RIGHTCENTER"
        return "RIGHTCENTER"
    if (indexOfLargest==4):
        print "MIDRIGHT"
        return "MIDRIGHT"
    if (indexOfLargest==5):
        print "FARRIGHT"
        return "FARRIGHT"

    print "FAILED INDEX"

    print "Reached end of function that is supposed to return a value"

###############################################################################

colourKey = {'black': makeColor( 20, 20, 20),
            'white': makeColor(255, 255, 255),
            'blue': makeColor( 50, 50, 255),
            'dark blue': makeColor( 20, 20, 100),
            'pink': makeColor(255, 175, 175),
            'red': makeColor(255, 50, 50),
            'dark red': makeColor(100, 20, 20),
            'grey': makeColor(128, 128, 128),
            'dark grey': makeColor( 64, 64, 64),
            'light grey': makeColor(192, 192, 192),
            'yellow': makeColor(255, 255, 0),
            'magenta': makeColor(255, 50, 255),
            'cyan': makeColor( 50, 255, 255),
            'purple': makeColor(127, 50, 255),
            'orange': makeColor(225,100, 50),
            'green': makeColor( 50, 255, 50),
            'dark green': makeColor(20, 100, 20)}

setIRPower = 130

def findColour(key):

    colour = colourKey[key]

    leftMotor = 1
    rightMotor = 1
    lastSeenPos = "NONE"
    counter = 0;
    while True:
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

            lastSeenPos = "NONE"
        if (direction=="FAILED"):
            #lastSeenPos = "FAILED"
            rightMotor = 0
            leftMotor = 0
        #print "UNKNOWN 'direction'"
        motors(leftMotor,rightMotor)

        numIter = 10
        total = 0
        for i in range(1,numIter+1):
            total += getObstacle("center")

        total /= numIter

        if (total >= 1100 and direction != "NONE"):
            motors(0,0)
            stop()
            marioOutro()
            break
    #stop();
#####################################################################
