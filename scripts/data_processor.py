#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class Processor():

	def __init__(self):
		rospy.Subscriber('/serial/drive',String,self.callbackDrive)
		rospy.Subscriber('/serial/robotic_arm',String,self.callbackRoboticArm)

		self.pubDrivePos = rospy.Publisher('/position/drive',String,queue_size=10)
		self.pubArmPos = rospy.Publisher('/position/robotic_arm',String,queue_size=10)

		self.rate = rospy.Rate(1)

	def callbackDrive(self,data):
		if self.checkDataType(data.data):
			print("Drive Data: "+ data.data)
			self.manipulate_and_publish(data.data)
		else:
			pass

	def callbackRoboticArm(self,data):
		if self.checkDataType(data.data):
			print("Robotic Arm Data: "+ data.data)
			self.manipulate_and_publish(data.data)
		else:
			pass

	def checkDataType(self,data_group):
		if (data_group[0] == 'A') and (data_group[-1] == 'B'):
			return True
		else:
			return False

	def manipulate_and_publish(self,data_group):
		num_of_motors = self.checkDataGroupLength(data_group)
		output_string = self.dataParser(data_group,num_of_motors)

		if num_of_motors == 4:
			self.pubDrivePos.publish(output_string)
		else:
			self.pubArmPos.publish(output_string)

	def checkDataGroupLength(self,data_group):
		length = len(data_group)
		length = (length-2)/4
		return length

	def dataParser(self,data_group,num_of_motors):
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
