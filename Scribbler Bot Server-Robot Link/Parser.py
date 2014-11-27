import random
import re
from Weather import *
from speakCustom import *

def contains(inputText, val):
	return val.lower() in inputText.lower();

def containsAll(inputText, vals):
	result = True
	for i in range(0,len(vals)):
		if (not vals[i].lower() in inputText.lower()):
			result = False
	return result

def containsOne(inputText, vals):
	result = False
	for i in range(0,len(vals)):
		if (vals[i].lower() in inputText.lower()):
			result = True
	return result

def elementInInput(inputText, elements):
	elementsInInput = []
	for i in range(0,len(elements)):
		if contains(inputText, elements[i]):
			elementsInInput.append(elements[i])
	longestMatch = elementsInInput[0]
	for i in range(1,len(elementsInInput)):
		if (len(elementsInInput[i]) > len(longestMatch)):
			longestMatch = elementsInInput[i]
	return longestMatch

def parse(inputText):
	inputText = inputText.lower().replace(" one ", " 1 ")
	inputText = inputText.lower().replace(" two ", " 2 ")
	inputText = inputText.lower().replace(" three ", " 3 ")
	inputText = inputText.lower().replace(" four ", " 4 ")
	inputText = inputText.lower().replace(" five ", " 5 ")

	function = ""
	arguments = []
	shouldSpeak = False
	colors = ["blue", "red", "dark red", "green", "dark green", "yellow", "magenta", "cyan", "purple", "orange"]
	pickUpLines = ["You make my software turn into hardware.", "Are you sitting on the F5 key? because your ass is refreshing.", "Want to see my HARD Disk? I promise it isn't 3.5 inches and it ain't floppy.", "I hope you're an I S O file, because I'd like to mount you."]
	jokesArray = ["You had me at Hello World.", "Failure is not an option. It comes bundled with your Scribbler Bot.", "There are only 10 types of people in the world: those that understand binary and those that don't.", "To err is human, and to blame it on a computer is even more so.", "CAPS LOCK, Preventing Login Since 1980", "If at first you don't succeed; call it version 1.0.", "My software never has bugs. It just develops random features", "If brute force doesn't solve your problems, then you aren't using enough.", "Latest survey shows that 3 out of 4 people make up 75 percent of the world's population."]
	comeAgainArray = ["come again?", "Sorry, I didn't quite catch that.", "I beg your pardon.", "What was that?"]
	modestComebacks = ["Thanks, I try my best.", "You're too nice.", "Right back atcha.", "Thanks"]
	helloArray = ["hello", "hi", "what's up", "sup", "yo"]
	name = "Buddy"

	inputNumbers = re.findall('\d+', inputText)


	
	if (containsOne(inputText, ["stop", "halt", "cancel"]) and containsOne(inputText, ["current"])):
		function = "stopCurrent"
	elif (containsOne(inputText, ["stop", "halt", "cancel"])):
		function = "stopAll"
	
	elif (containsOne(inputText, ["find", "look for", "follow", "go to"]) and containsOne(inputText, colors)):
		function = "findColour"
		arguments.append(elementInInput(inputText, colors))
	elif (containsOne(inputText, ["find", "look for", "follow", "go to"]) and len(inputNumbers) > 0 and containsOne(inputText, ["colour", "color"])):
		function = "rememberColours"
		arguments.append(int(inputNumbers[0]))
	
	elif (containsAll(inputText, ["play", "mario"])):
		if (contains(inputText, "outro")):
			function = "marioOutro"
		else:
			function = "marioIntro"
			shouldSpeak = True
	elif (containsAll(inputText, ["play", "cat"])):
		function = "nyanCat"
	elif (containsAll(inputText, ["play", "star", "wars"])):
		function = "starWars"
	elif (containsAll(inputText, ["play", "sand", "storm"])):
		function = "darude"
	
	elif (containsOne(inputText, ["move", "drive"]) and contains(inputText, "forward")):
		function = "moveStraight"
		if (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
	elif (containsOne(inputText, ["move", "drive"]) and contains(inputText, "backward")):
		function = "moveStraight"
		if (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
		else:
			arguments.append(3)
		arguments.append(-1)
	elif (containsAll(inputText, ["turn", "right"])):
		function = "turnRightByDegrees"
		if (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
	elif (containsAll(inputText, ["turn", "left"])):
		function = "turnLeftByDegrees"
		if (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
	elif ((containsOne(inputText, ["turn", "point"]) and containsOne(inputText, ["at", "to"])) or
		(contains(inputText, "point") and containsOne(inputText, ["north", "south", "east", "west"]))):
		function = "turnToDegrees"
		if (contains(inputText, "north")):
			arguments.append(0)
		elif (contains(inputText, "south")):
			arguments.append(180)
		elif (contains(inputText, "west")):
			arguments.append(90)
		elif (contains(inputText, "east")):
			arguments.append(270)
		elif (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
	elif ((containsOne(inputText, ["mimic", "copy", "follow"]) and contains(inputText, "compass")) or 
		containsOne(inputText, ["align", "synchonize"]) and contains(inputText, "me")):
		function = "followCompass"

	elif (containsOne(inputText, ["drive", "race"])):
		function = "myoDrive"

	elif (containsAll(inputText, ["What", "your", "name"])):
		function = "speakCustom"
		arguments.append("Hi. My name is "+name)
	elif (containsAll(inputText, [name, "Speak"])):
		function = "speakCustom"
		arguments.append("Your not my motherboard")
	elif (containsAll(inputText, [name, "tell", "joke"])):
		function = "speakCustom"
		arguments.append(random.choice(jokesArray))
	elif (containsAll(inputText, [name, "pick", "up", "line"])):
		function = "speakCustom"
		arguments.append(random.choice(pickUpLines))
	elif (containsAll(inputText, [name, "homework"])):
		function = "speakCustom"
		arguments.append("do I look like Wolfram Alpha")
	elif (containsAll(inputText, [name, "pump", "up"])):
		function = "speakCustom"
		arguments.append("your not an inflatable balloon")
	elif (containsAll(inputText, [name, "roll", "over"])):
		function = "speakCustom"
		arguments.append("I'm a companion. not a dog")
	elif (containsAll(inputText, [name, "boy", "girl"])):
		function = "speakCustom"
		arguments.append("I'm just happy to see you. Nudge nudge wink wink")
	elif (containsAll(inputText, [name, "I", "sad"])):
		function = "speakCustom"
		arguments.append("don't bring me down.......... just kidding. I love you")
	elif (containsOne(inputText, ["best", "awesome", "good job", "nice"])):
		function = "speakCustom"
		arguments.append(random.choice(modestComebacks))
	elif (containsOne(inputText, ["hello", "hi"])):
		function = "speakCustom"
		arguments.append(random.choice(helloArray))
	elif (containsOne(inputText, ["temperature"])):
		function = "speakCustom"
		arguments.append(WhatIsTheTemperature())
	elif (containsOne(inputText, ["weather"])):
		function = "speakCustom"
		arguments.append(WhatIsTheWeather())
	elif (containsOne(inputText, ["umbrilla"])):
		function = "speakCustom"
		arguments.append(DoINeedAnUmbrella())
	elif (containsOne(inputText, ["shorts"])):
		function = "speakCustom"
		arguments.append(ShouldIWearShorts())
	
	for i in range(0, len(arguments)):
		if isinstance(arguments[i], basestring):
			arguments[i] = '"'+arguments[i]+'"'
	
	if (function != ""):
		if (function == "speakCustom"):
			speakCustom(''.join(str(x) for x in arguments))
			command = ""
		else:
			command = function+'('+', '.join(str(x) for x in arguments)+')'

		if shouldSpeak:
			command = 'speakCustom('+command.rstrip()+')'
	else:
		command = ""
		speakCustom(random.choice(comeAgainArray))

	return command
