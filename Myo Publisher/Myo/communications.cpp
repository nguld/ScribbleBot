//
//  main.cpp
//  Hackathon
//
//  Created by Gillian Maducdoc, Jitin Dodd, Justin Stribling, Mart van Buren on 2014-11-01.
//  Copyright (c) 2014 Group 16. All rights reserved.
//

#include "communications.h"

#include <stdio.h>

#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <algorithm>

int currentComputer = 0;
int totalComputers = 0;

/* CONNECTION INFO */
// Local
    //std::string redisConnectionInfo = "";
// Public Server - For iPhone Sensor Data
    //std::string redisConnectionInfo = "-h pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com -p 10592 -a GiJiJuKaMaNoRo";
// Public Server - For Myo Data
    std::string redisConnectionInfo = "-h pub-redis-10683.us-east-1-2.5.ec2.garantiadata.com -p 10683 -a GiJiJuKaMaNoRo";

int numSubscribers() {
    if (totalComputers == -1) {
        std::string output;
        
        std::string command = "/usr/local/bin/redis-cli "+redisConnectionInfo+" PUBSUB NUMSUB engHack16";
        std::string str = command;
        char * writable = new char[str.size() + 1];
        std::copy(str.begin(), str.end(), writable);
        writable[str.size()] = '\0';
        
        output = exec(writable);
        
        delete[] writable;
        
        std::string lastLine;
        std::istringstream f(output);
        std::string line;
        while (std::getline(f, line)) {
            lastLine = line;
        }
        
        return atoi(lastLine.c_str());
    } else {
        return totalComputers;
    }
}

std::string exec(char* cmd) {
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while(!feof(pipe)) {
        if(fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }
    pclose(pipe);
    return result;
}

void redisSetKey(std::string key, std::string value) {
    std::string command = "/usr/local/bin/redis-cli "+redisConnectionInfo+" set " + key + " " + value;
    std::string str = command;
    char * writable = new char[str.size() + 1];
    std::copy(str.begin(), str.end(), writable);
    writable[str.size()] = '\0';
    
    exec(writable);
    
    delete[] writable;
}
void redisPublish(std::string value, std::string channel) {
    std::string command = "/usr/local/bin/redis-cli "+redisConnectionInfo+" PUBLISH scribbler"+channel+" " + value;
    std::string str = command;
    char * writable = new char[str.size() + 1];
    std::copy(str.begin(), str.end(), writable);
    writable[str.size()] = '\0';
    
    exec(writable);
    
    delete[] writable;
}
void redisPublishArray(int elements[3], std::string channel) {
    std::string publish = "[" + std::to_string(elements[0]) + "," + std::to_string(elements[1]) + "," + std::to_string(elements[2]) + "]";
    redisPublish(publish, channel);
}

void newPose(std::string pose) {
    redisPublish(pose, "MyoPoses");
}
void newSensorData(int roll, int pitch, int yaw) {
    int elements[] = {roll, pitch, yaw};
    redisPublishArray(elements, "MyoSensors");
}

void initialSetup() {
    totalComputers = numSubscribers();
    std::cout << std::to_string(totalComputers) << " Subscribers" << std::endl;
}