#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class Processor():

	def __init__(self):

		rospy.init_node("data_processor")
		rospy.Subscriber('/serial/drive',String,self.callback)
		rospy.Subscriber('/serial/robotic_arm',String,self.callback)

		self.pubDrivePos = rospy.Publisher('/position/drive',String,queue_size=10)
		self.pubArmPos = rospy.Publisher('/position/robotic_arm',String,queue_size=10)

	def callback(self,data):
		if data.data[0] == 'A' and data.data[-1] == 'B':
			self.manipulateAndPublish(data.data)
		else:
			print("False data: " + data.data)

	def manipulateAndPublish(self,data_group):
		num_of_motors = self.getDataGroupLength(data_group)
		output_string = self.parseData(data_group,num_of_motors)

		if num_of_motors == 4:
			print("Drive: " + data_group + "\nPublishing: " + output_string)
			self.pubDrivePos.publish(output_string)
		elif num_of_motors == 6:
			print("Robotic arm: " + data_group + "\nPublishing: " + output_string)
			self.pubArmPos.publish(output_string)

	def getDataGroupLength(self,data_group):
		length = len(data_group)
		length = (length-2)/4
		return length

	def parseData(self,data_group,num_of_motors):
		initial_point = 2
		parsed_data = ""

		for i in range(0,num_of_motors):
			speed = int(data_group[initial_point:initial_point+3])
			speed = self.checkMagnitude(speed)
			sign_num = data_group[initial_point-1]
			speed = str(self.detectSign(speed,sign_num))
			parsed_data = parsed_data + speed + " "
			initial_point += 4

		parsed_data = parsed_data[0:-1]
		return parsed_data		

	def checkMagnitude(self,speed):
		if (speed > 255):
			speed = 255
		return speed

	def detectSign(self,speed,sign_num):
		if (sign_num == '1'):
			speed *= -1
		return speed

if __name__ == "__main__":
	p = Processor()
	rospy.spin()