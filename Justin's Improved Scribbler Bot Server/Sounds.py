from myro import *

def marioIntro():
	marioIntro = makeSong("e6 0.25; e6 0.5; e6 0.6; c6 0.25; e6 0.5; g6 1; g5 0.5")
	playSong(marioIntro)
	return "Mario"

def nyanCat():
	nyanCat = makeSong("f#5 0.3; ab5 0.3; eb5 0.15; eb5 0.15; b4 0.3; d5 0.15; db5 0.15; b4 0.3; b4 0.3; db5 0.3; d5 0.3; d5 0.15; db5 0.15; b4 0.15; db5 0.15; eb5 0.15; f#5 0.15; ab5 0.15; eb5 0.15; f#5 0.15; db5 0.15; eb5 0.15; b4 0.15; db5 0.15; b4 0.15; eb5 0.3; f#5 0.3; ab5 0.3; eb5 0.15; f#5 0.15; db5 0.15; eb5 0.15; b4 0.15; d5 0.15; eb5 0.15; d5 0.15; db5 0.15; b4 0.15; db5 0.15; d5 0.15; b4 0.3; db5 0.15; eb5 0.15; f#5 0.15; db5 0.15; eb5 0.15; db5 0.15; b4 0.15; db5 0.3; b4 0.3")
	playSong(nyanCat)

def starWars():
	starWars = makeSong("bb5 1.5; f6 1; eb6 0.2; d6 0.2; c6 0.2; bb6 1; f6 0.8; eb6 0.2; d6 0.2; c6 0.2; bb6 1; f6 0.8; eb6 0.2; d6 0.2; eb6 0.2; c6 1")
	playSong(starWars)

def darude():
	darude = makeSong("b5 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2; b5 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2; e6 0.3; e6 0.05; e6 0.05; e6 0.05; e6 0.05; e6 0.3; d6 0.05; d6 0.05; d6 0.05; d6 0.05; d6 0.3; d6 0.3; a5 0.5; b5 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2; b2 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2; b5 0.3; d6 0.3; b5 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2; b5 0.05; b5 0.05; b5 0.05; b5 0.05; b5 0.2;")
	playSong(darude)

def marioOutro():
	marioOutro = makeSong("b5 0.2; f6 0.5; f6 0.2; f6 0.3; e6 0.2; d6 0.2; c6 0.3; g5 0.3; e5 0.3; c5 0.6")
	playSong(marioOutro)