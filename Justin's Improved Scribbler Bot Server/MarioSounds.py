from myro import *

def marioIntro():
	marioIntro = makeSong("e6 0.25; e6 0.5; e6 0.6; c6 0.25; e6 0.5; g6 1; g5 0.5")
	playSong(marioIntro)
	return "Mario"

def marioOutro():
	marioOutro = makeSong("b5 0.2; f6 0.5; f6 0.2; f6 0.3; e6 0.2; d6 0.2; c6 0.3; g5 0.3; e5 0.3; c5 0.6")
	playSong(marioOutro)
	return "Mario"