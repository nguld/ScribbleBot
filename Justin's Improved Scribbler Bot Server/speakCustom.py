import subprocess
import sys
def speakCustom(text):
	a = subprocess.Popen(["redis-cli", "-h", "pub-redis-16825.us-east-1-2.5.ec2.garantiadata.com", "-p", "16825", "-a", "GiJiJuKaMaNoRo", "publish", "scribblerPhoneCommands", 'speak("' + text + '")'], shell=False, stdout=subprocess.PIPE)