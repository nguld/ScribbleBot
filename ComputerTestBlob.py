from math import *
from myro import *

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


while 1:
    colour = input("Enter Colour: ")
    #colour = blue

    #pic = takePicture() #Uncomment this for robot

    pic = makePicture("/Users/Karel/Desktop/stripes.gif") #jpg or gif only

    show(pic)

    colourTollerance = 100

    RGBred, RGBgreen, RGBblue = getRGB(colour);

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
            if (abs(r - RGBred) < colourTollerance) and (abs(g - RGBgreen) < colourTollerance) and (abs(b - RGBblue) < colourTollerance):
                setRGB(pixel, (255,255,255))
                if (i < w/3):
                    leftSideTotal += 1
                elif (i > w/3):
                    rightSideTotal += 1
                else:
                    centerTotal += 1
            else:
                setRGB(pixel, (0,0,0))
            setPixel(pic, i, j, pixel)

    show(pic)

    errorTollerance = 10

    #determine direction
    if (abs(leftSideTotal - centerTotal) < errorTollerance and abs(leftSideTotal - rightSideTotal) < errorTollerance and abs(rightSideTotal - centerTotal) < errorTollerance):
        direction = "NONE"

    if (leftSideTotal > centerTotal and leftSideTotal > rightSideTotal):
        direction = "LEFT"
    elif (rightSideTotal > centerTotal and rightSideTotal > leftSideTotal):
        direction = "RIGHT"
    else:
        direction = "CENTER"

    print direction
