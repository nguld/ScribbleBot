import random
import re

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
	function = ""
	arguments = []
	shouldSpeak = False
	colors = ["blue", "red", "dark red", "green", "dark green", "yellow", "magenta", "cyan", "purple", "orange"]
	jokesArray = ["You make my software turn into hardware", "Are you sitting on the F5 key? because your ass is refreshing.", "You had me at Hello World", "Want to see my HARD Disk? I promise it isn't 3.5 inches and it ain't floppy", "I hope you're an I S O file, because I'd like to mount you."]
	name = "romeo"

	inputNumbers = re.findall('\d+', inputText)

	if (containsAll(inputText, ["round", "box"])):
		function = "aroundBox";
		if (contains(inputText, "angle")):
			arguments.append(1)
			arguments.append(1)
		shouldSpeak = True
	
	elif (containsOne(inputText, ["stop", "halt", "cancel"]) and containsOne(inputText, ["current"])):
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
	elif (containsAll(inputText, ["play", "nyan", "cat"])):
		function = "nyanCat"
	elif (containsAll(inputText, ["play", "star", "wars"])):
		function = "starWars"
	elif (containsAll(inputText, ["play", "sand", "storm"])):
		function = "darude"
	
	elif (containsAll(inputText, ["move", "forward"])):
		function = "moveStraight"
		if (len(inputNumbers) > 0):
			arguments.append(int(inputNumbers[0]))
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
	elif (containsOne(inputText, ["mimic", "copy", "follow"]) and contains(inputText, "compass")):
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
	elif (containsAll(inputText, [name, "math", "homework"])):
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
	elif (containsAll(inputText, [name, "your", "best"])):
		function = "speakCustom"
		arguments.append("no you")
	elif (containsAll(inputText, [name, "no", "you"])):
		function = "speakCustom"
		arguments.append("no you")
	elif (containsAll(inputText, [name, "I", "sad", "am"])):
		function = "speakCustom"
		arguments.append("don't bring me down.......... just kidding. I love you")
	elif (containsAll(inputText, [name, "set", "up"])):
		function = "speakCustom"
		arguments.append("Hey ladies, are you on or below the crazy hot line?")
	
	for i in range(0, len(arguments)):
		if isinstance(arguments[i], basestring):
			arguments[i] = '"'+arguments[i]+'"'
	
	if (function != ""):
		command = function+'('+', '.join(str(x) for x in arguments)+')'
		if shouldSpeak:
			command = 'speakCustom('+command.rstrip()+')'
	else:
		command = 'speakCustom("'+inputText.rstrip()+'")'

	return command
