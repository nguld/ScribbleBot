#see colours and remember them

from math import *
from myro import *
from FindObject import *

###################################################
#                 Define Colours                  #
###################################################
# black =     makeColor( 0, 0, 0)
# white =     makeColor(255, 255, 255)
blue =      makeColor( 0, 0, 255)
# darkBlue =  makeColor( 0, 0, 100)
# pink =      makeColor(255, 175, 175)
red =       makeColor(255, 0, 0)
darkRed =   makeColor(100, 0, 0)
# green =     makeColor( 0, 255, 0)
darkGreen = makeColor(0, 100, 0)
# grey =      makeColor(128, 128, 128)
# darkGrey =  makeColor( 64, 64, 64)
# lightgrey = makeColor(192, 192, 192)
yellow =    makeColor(255, 255, 0)
magenta =   makeColor(255, 0, 255)
# cyan =      makeColor( 0, 255, 255)
# purple =    makeColor(127, 0, 255)
# orange =    makeColor(225,100, 0)
# brown = 	makeColor(102, 51, 0)


def seeColor ():#this takes a picture, finds average RGB code
	avgR = 0
	avgG = 0
	avgB = 0
	r = []
	g = []
	b = []
	pic = takePicture()
	#pic = makePicture(pickAFile())
	beep(0.5, 550)
	wait(1)
	#show(pic)
	width = getWidth(pic)
	height = getHeight(pic)
	for x in range (1, width):
		for y in range (1, height):
			pixel = getPixel(pic, x, y)
			#r[len(r):], g[len(g):], b[len(b):] = getRGB(pixel)
			r.append(getRed(pixel))
			g.append(getGreen(pixel))
			b.append(getBlue(pixel))
	
	for a in range (len(r)):
		avgR = avgR + r[a]
		avgB = avgB + b[a]
		avgG = avgG + g[a]
		
	avgR = avgR / len(r)
	avgG = avgG / len(g)
	avgB = avgB / len(b)
	
	print"R %d  G %d  B %d" % (avgR, avgG, avgB) 
	
	myColour = makeColor(avgR, avgG, avgB)
	#W = H = 100
	#newPic = makePicture(W, H, myColour)
	#show(newPic)
	return avgR, avgG, avgB
	
def determineColor ():#this takes a color from a picture and gives it a name
	listColors = [blue, red, darkRed, darkGreen, yellow, magenta]
	dictColors = {blue: 'blue', red: 'red', darkRed: 'dark red', darkGreen: 'dark green', yellow: 'yellow',magenta: 'magenta'}
	
	color = makeColor(seeColor())
	listDifference = []
		
	for i in range (len(listColors)):
		r = abs(getRed(color) - getRed(listColors[i]))
		g = abs(getGreen(color) - getGreen(listColors[i]))
		b = abs(getBlue(color) - getBlue(listColors[i]))
		listDifference.append(sqrt(pow(r,2) + pow(g,2) + pow(b,2)))
     
	 
	for j in range (len(listDifference)):
		#print listDifference[j]
		if (j == 0):
			minDiff = listDifference[j]
			location = 0
		elif (listDifference[j] < minDiff):
			minDiff = listDifference[j]			
			location = j

	myColor = listColors[location]
	for key in dictColors:
		if (myColor == key):
			colorName = dictColors[key]
			#sequenceColors.append(dictColors[key])
	#print myColor
	return colorName
	
def goToColors(listC):
	for m in range (len(listC)):
		findColour(listC[m])
	
def rememberColours (num):
	listColours = []
	i = 0
	#while timeRemaining(30):
	for m in range (0, num):
		color = determineColor()
		listColours.append(color)
		#show(newPic)
	print listColours[:]
	goToColors(listColours)