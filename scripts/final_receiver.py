#!/usr/bin/env python

import rospy
from std_msgs.msg import String


def callbackDrive(data):
    print("Drive Position: " + data.data)

def callbackRoboticArm(data):
    print("Robotic Arm Position: " + data.data)

def final_receiver():
    
    rospy.init_node('final_receiver')

    rospy.Subscriber("/position/drive", String, callbackDrive)
    rospy.Subscriber("/position/robotic_arm", String, callbackRoboticArm)

    rospy.spin()

if __name__ == '__main__':
    final_receiver()
