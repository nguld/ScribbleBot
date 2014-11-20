//
//  main.cpp
//  Hackathon
//
//  Created by Gillian Maducdoc, Jitin Dodd, Justin Stribling, Mart van Buren on 2014-11-01.
//  Copyright (c) 2014 Group 16. All rights reserved.
//

#include <stdio.h>

#define _USE_MATH_DEFINES
#include <cmath>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <algorithm>
#include <cstdio>
#include <ctime>

#include "/Users/martvanburen/Dropbox/Documents/UWaterloo/SE101/MyoPublisher/myo.framework/Headers/myo.hpp"

#include "communications.h"

int showSensorData = 0;

class MyoListener : public myo::DeviceListener {
public:
    
    std::string lastPose;
    std::string secondLastPose;
    
    int roll_w;
    int pitch_w;
    int yaw_w;
    
    float roll_f;
    float pitch_f;
    float yaw_f;
    
    float last_roll;
    float last_pitch;
    float last_yaw;
    
    void onOrientationData(myo::Myo* myo, uint64_t timestamp, const myo::Quaternion<float>& quat)
    {
        using std::atan2;
        using std::asin;
        using std::sqrt;
        using std::max;
        using std::min;
        
        // Calculate Euler angles (roll, pitch, and yaw) from the unit quaternion.
        float roll = atan2(2.0f * (quat.w() * quat.x() + quat.y() * quat.z()),
                           1.0f - 2.0f * (quat.x() * quat.x() + quat.y() * quat.y()));
        float pitch = asin(max(-1.0f, min(1.0f, 2.0f * (quat.w() * quat.y() - quat.z() * quat.x()))));
        float yaw = atan2(2.0f * (quat.w() * quat.z() + quat.x() * quat.y()),
                          1.0f - 2.0f * (quat.y() * quat.y() + quat.z() * quat.z()));
        
        roll_f = ((roll + (float)M_PI)/(M_PI * 2.0f) * 18);
        pitch_f = ((pitch + (float)M_PI/2.0f)/M_PI * 18);
        yaw_f = ((yaw + (float)M_PI)/(M_PI * 2.0f) * 18);
        
        // Convert the floating point angles in radians to a scale from 0 to 18.
        roll_w = static_cast<int>((roll + (float)M_PI)/(M_PI * 2.0f) * 18);
        pitch_w = static_cast<int>((pitch + (float)M_PI/2.0f)/M_PI * 18);
        yaw_w = static_cast<int>((yaw + (float)M_PI)/(M_PI * 2.0f) * 18);
        if (showSensorData)
            std::cout << "Roll: " << roll_w << " | Pitch: " << pitch_w << " | Yaw: " << yaw_w << std::endl;
        
        if (roll_w != (int)last_roll || pitch_w != (int)last_pitch || yaw_w != (int)last_yaw)
            newSensorData(roll_w, pitch_w, yaw_w);
        
        last_roll = roll_f;
        last_pitch = pitch_f;
        last_yaw = yaw_f;
    }
    
    void onPair(myo::Myo* myo, uint64_t timestamp, myo::FirmwareVersion firmwareVersion)
    {
        knownMyos.push_back(myo);
        std::cout << "Paired with " << identifyMyo(myo) << " Myo" << std::endl;
    }
    
    void onPose(myo::Myo* myo, uint64_t timestamp, myo::Pose pose)
    {
        std::string poseString = pose.toString();
        secondLastPose = lastPose;
        lastPose = poseString;
        
        newPose(poseString);
        newSensorData(roll_w, pitch_w, yaw_w);
        
        poseString += " (Roll: " + std::to_string((int)roll_w) + ")";
        std::cout << "Myo " << identifyMyo(myo) << " switched to pose " << poseString << "." << std::endl;
    }
    
    void onConnect(myo::Myo* myo, uint64_t timestamp, myo::FirmwareVersion firmwareVersion)
    {
        std::cout << "Myo " << identifyMyo(myo) << " has connected." << std::endl;
    }
    
    size_t identifyMyo(myo::Myo* myo) {
        for (size_t i = 0; i < knownMyos.size(); ++i) {
            if (knownMyos[i] == myo) {
                return i + 1;
            }
        }
        return 0;
    }
    
    void onDisconnect(myo::Myo* myo, uint64_t timestamp)
    {
        std::cout << "Myo " << identifyMyo(myo) << " has disconnected." << std::endl;
    }
    
    std::vector<myo::Myo*> knownMyos;
};

int main(int argc, const char * argv[]) {
    initialSetup();
    
    try {
        myo::Hub hub("com.hackathon.myo");
        
        // Instantiate the PrintMyoEvents class we defined above, and attach it as a listener to our Hub.
        MyoListener listener;
        hub.addListener(&listener);
        
        while (1) {
            // Process events for 10 milliseconds at a time.
            hub.run(10);
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cerr << "Press enter to continue.";
        std::cin.ignore();
    }
}