//
//  main.cpp
//  Hackathon
//
//  Created by Gillian Maducdoc, Jitin Dodd, Justin Stribling, Mart van Buren on 2014-11-01.
//  Copyright (c) 2014 Group 16. All rights reserved.
//

#ifndef __Myo__communications__
#define __Myo__communications__

#include <stdio.h>

#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <algorithm>

int numSubscribers();

std::string exec(char* cmd);
void redisSetKey(std::string key, std::string value);
void redisPublishArray(float elements[3], std::string channel);

void newPose(std::string pose);
void newSensorData(int roll, int pitch, int yaw);

void initialSetup();

#endif /* defined(__Myo__communications__) */
