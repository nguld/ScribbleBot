from myro.simlator import *

def INIT():
	# (width, height), (offset x, offset y), scale:
    sim = TkSimulator((425,423), (5,420), 208.005558)
    # x1, y1, x2, y2 in meters:
    sim.addBox(0, 0, 2, 2)
    #sim.addLight(.25, .25, 1.0) # x, y, brightness
    sim.addRobot(60000, TkMyro("BlueMyro",
                               1.69, 1.68, 2.03,
                               ((.09, .09,-.09,-.09),
                                (.08,-.08,-.08, .08)), "blue"))
    for i in range(len(sim.robots)):
        #sim.robots[i].addDevice(BulbDevice(-.10, 0))
        sim.robots[i].addDevice(MyroIR()) # infrared
        #sim.robots[i].addDevice(MyroBumper()) # bumpers
        sim.robots[i].addDevice(MyroLightSensors()) # light sensors 
        sim.robots[i].addDevice(MyroLineSensors()) # downward-facing sensor


	return sim