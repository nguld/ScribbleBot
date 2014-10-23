from math import *

###################################################
#                 Define Colours                  #
###################################################
black = makeColor( 0, 0, 0)
white = makeColor(255, 255, 255)
blue = makeColor( 0, 0, 255)
red = makeColor(255, 0, 0)
green = makeColor( 0, 255, 0)
gray = makeColor(128, 128, 128)
darkGray = makeColor( 64, 64, 64)
lightGray = makeColor(192, 192, 192)
yellow = makeColor(255, 255, 0)
pink = makeColor(255, 175, 175)
magenta = makeColor(255, 0, 255)
cyan = makeColor( 0, 255, 255)
###################################################



#pic = takePicture()

pic = makePicture(“directory/nameOfPic.jpg”) #jpg or gif only

#
tollerance = 50
colour = pink

red, green, blue = getRGB(colour);

for pixel in getPixel(pic)
    r, g, b = getRGB(pixel)
    if (abs(r - red) < tollerance) && (abs(g - green) < tollerance) && (abs(b - blue) < tollerance)
        setRGB(pixel, (255,255,255))
    else:
        setRGB(pixel, (0,0,0))
show(pic)
