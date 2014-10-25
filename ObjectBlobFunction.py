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
orange =     makeColor(225,100, 0)
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

def determineDirection (colour):

    pic = takePicture() #Uncomment this for robot

    #pic = makePicture("/Users/Karel/Desktop/stripes.gif") #jpg or gif only

    RGBred, RGBgreen, RGBblue = getRGB(colour);
    #print "|" , RGBred , "|" , RGBgreen , "|" , RGBblue , "|"

    h = getHeight(pic)
    w = getWidth(pic)

    # Variable for image analysis
    leftSideTotal = 0
    rightSideTotal = 0
    centerTotal = 0



    for i in range(1, w):
        for j in range(1, h):
            pixel = getPixel(pic, i, j)
            r, g, b = getRGB(pixel)

            # FORMULA 1
            distanceFrom = sqrt(pow(abs(r-RGBred),2) + pow(abs(g-RGBgreen),2) + pow(abs(b-RGBblue),2))
            if (distanceFrom < 100):
            #################################################################

            #FORMULA 2
            #distanceFrom = abs(r-RGBred) + abs(g-RGBgreen) + abs(b-RGBblue)
            #if (distanceFrom < 120):
            #################################################################

                #setRGB(pixel, (255,255,255))

                if (i < w/3):
                    leftSideTotal += 1
                elif (i > w - (w/3)):
                    rightSideTotal += 1
                else:
                    centerTotal += 1
            else:
                setRGB(pixel, (0,0,0))

            #setPixel(pic, i, j, pixel)

    errorTollerance = 10

    #determine direction
    if (abs(leftSideTotal - centerTotal) < errorTollerance and abs(leftSideTotal - rightSideTotal) < errorTollerance and abs(rightSideTotal - centerTotal) < errorTollerance):
        return "NONE"

    if (leftSideTotal > centerTotal and leftSideTotal > rightSideTotal):
        return "LEFT"
    elif (rightSideTotal > centerTotal and rightSideTotal > leftSideTotal):
        return "RIGHT"
    else:
        return "CENTER"
