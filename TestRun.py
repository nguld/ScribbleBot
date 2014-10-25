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
orange =     makeColor(225,100, 0)


while True:

    direction = determineDirection(red)

    if (direction == "NONE"):
        turnRight(1,1)
    elif (direction == "LEFT"):
        turnLeft(1,1)
    elif (direction == "RIGHT"):
        turnRight(1,1)
    elif (direction == "CENTER"):
        forward(1,1)
