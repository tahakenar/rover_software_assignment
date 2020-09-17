#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class Processor():

	def __init__(self):
		rospy.Subscriber('/serial/drive',String,self.callback)
		rospy.Subscriber('/serial/robotic_arm',String,self.callback)

		self.pubDrivePos = rospy.Publisher('/position/drive',String,queue_size=10)
		self.pubArmPos = rospy.Publisher('/position/robotic_arm',String,queue_size=10)

		self.rate = rospy.Rate(1)

	def callback(self,data):
		if self.checkDataType(data.data):
			self.manipulate_and_publish(data.data)
		else:
			pass

	def checkDataType(self,data_group):
		if (data_group[0] == 'A') and (data_group[-1] == 'B'):
			return True
		else:
			return False

	def manipulate_and_publish(self,data_group):
		num_of_motors = self.getDataGroupLength(data_group)
		output_string = self.parseData(data_group,num_of_motors)

		if num_of_motors == 4:
			print("Drive data: " + data_group)
			self.pubDrivePos.publish(output_string)
		else:
			print("Robotic arm data: " + data_group)
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
			directionNum = data_group[initial_point-1]
			speed = str(self.detectDirection(speed,directionNum))
			parsed_data = parsed_data + speed + " "
			initial_point += 4

		parsed_data = parsed_data[0:-1]
		return parsed_data		

	def checkMagnitude(self,speed):
		if (speed > 255):
			speed = 255
		return speed

	def detectDirection(self,speed,directionNum):
		if (directionNum == '1'):
			speed *= -1
		return speed

if __name__ == "__main__":
	rospy.init_node("data_processor")
	p = Processor()
	rospy.spin()