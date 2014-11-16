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
	shouldSpeak = True
	colors = ["black", "white", "blue", "dark blue", "pink", "red", "dark red", "green", "dark green", "gray", "dark gray", "light gray", "yellow", "magenta", "cyan", "purple", "orange"]
	
	if (containsAll(inputText, ["round", "box"])):
		function = "aroundBox";
		if (contains(inputText, "angle")):
			arguments.append(1)
			arguments.append(1)
	elif (containsOne(inputText, ["stop", "halt", "cancel"]) and containsOne(inputText, ["current"])):
		function = "stopCurrent"
		shouldSpeak = false
	elif (containsOne(inputText, ["stop", "halt", "cancel"])):
		function = "stopAll"
		shouldSpeak = false
	elif (containsOne(inputText, ["find", "look for", "follow", "go to"]) and containsOne(inputText, colors)):
		function = "findColour"
		arguments.append(elementInInput(inputText, colors))
	elif (containsAll(inputText, ["play", "mario"])):
		if (contains(inputText, "outro")): function = "marioOutro"
		else: function = "marioIntro"
	
	for i in range(0, len(arguments)):
		if isinstance(arguments[i], basestring):
			arguments[i] = '"'+arguments[i]+'"'
	
	if (function != ""):
		command = function+'('+', '.join(str(x) for x in arguments)+')'
		if shouldSpeak: command = 'speakCustom('+command+')'
	else:
		command = 'speakCustom("'+inputText+'")'

	return command
