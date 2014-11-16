# Parameter : input colour (defined below)
# Return    : direction ('LEFT', 'RIGHT', 'CENTER')

from math import *
from myro import *

###################################################
#                 Define Colours                  #
###################################################
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
###################################################



###################################################
#                Image Processing                 #
###################################################
#
# 1) Change pixel colour based on colour tollerance
#
# 2) Determines what side of the picture the
#    majority of the pixels are on
#
###################################################
def determineDirection (colour, num):

    pic = takePicture() #Uncomment this for robot

    #path = os.path.dirname(os.path.realpath(__file__))
    #pic = makePicture(path + "/lucy.gif") #jpg or gif only

    RGBred, RGBgreen, RGBblue = getRGB(colour);
    #print "|" , RGBred , "|" , RGBgreen , "|" , RGBblue , "|"

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


    for i in range(1, w, 4):
        for j in range(1, h, 4):
            pixel = getPixel(pic, i, j)
            r, g, b = getRGB(pixel)

            # FORMULA 1
            distanceFrom = sqrt((r - RGBred)*(r - RGBred) + (g - RGBgreen)*(g - RGBgreen) + (b - RGBblue)*(b - RGBblue));
            #distanceFrom = sqrt(pow(abs(r-RGBred),2) + pow(abs(g-RGBgreen),2) + pow(abs(b-RGBblue),2))
            if (distanceFrom < 100):
                setRGB(pixel, (255,255,255))
                for index in range(0,6):
                    if i > (index) * (w/6): #Check if greater then lower
                        if i < (index+1) * (w/6):
                            totalArray[index] += 1
                            break
            else:
                setRGB(pixel, (0,0,0))
            setPixel(pic, i/4, j/4, pixel)

    ####################
    #for t in totalArray:
    #    print "| " , t , " "
    outputFile = "lucyProcessed" + str(num) + ".gif"
    #print outputFile
    savePicture(pic, outputFile)
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

#determineDirection(pink,1)