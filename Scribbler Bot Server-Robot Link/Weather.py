import urllib
import json
import re

f = urllib.urlopen("http://api.wunderground.com/api/698b8e12c86cc092/conditions/q/Canada/Kitchener-Waterloo_Regional.json")
json_string = f.read()
parsed_json = json.loads(json_string)


def WhatIsTheTemperature():
	temp_c = parsed_json['current_observation']['temp_c']
	feelstemp_c = parsed_json['current_observation']['windchill_c']
	str = ""
	if float(temp_c) < 0:
		str = "It is cold out. "
	elif float(temp_c) > 0:
		str = "It is warm out. "
	str += "it is currently %s degrees" % temp_c
	if float(temp_c) != float(feelstemp_c):
		str += " but it feels like %s." % feelstemp_c
	return str

def WhatIsTheWeather():
	temp_c = parsed_json['current_observation']['temp_c']
	feelstemp_c = parsed_json['current_observation']['windchill_c']
	wind_kph = parsed_json['current_observation']['wind_kph']
	gust_kph = parsed_json['current_observation']['wind_gust_kph']
	wind_Dir = parsed_json['current_observation']['wind_dir']
	str = "it is currently %s degrees" % temp_c
	if float(temp_c) != float(feelstemp_c):
		str += " but it feels like %s due to a %s gusting up to %s from the %s" % (feelstemp_c, wind_kph, gust_kph, wind_Dir)
	return str

def DoINeedAnUmbrella():
	humidity_dirty = parsed_json['current_observation']['relative_humidity']
	humidity_clean = re.sub('%','', humidity_dirty)
	weather = parsed_json['current_observation']['weather']
	str = "the weather is currently %s with a %s percent humidity. You tell me if you need an umbrella" % (weather, humidity_clean)
	return str

def ShouldIWearShorts():
	feelstemp_c = parsed_json['current_observation']['windchill_c']
	str = ""
	if float(feelstemp_c) > -5:
		if float(feelstemp_c) < 10:
			str = "If you are Keith yes. Otherwise it's a bit cold out don't you think?"
		else:
			str = "Sure. It's warm enough"
	if float(feelstemp_c) < -5:
		str = "it's too cold for shorts. Even if you are Keith"
	return str
	

f.close()