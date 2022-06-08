#!/usr/bin/env python
#Source Code for Turtle 2
#chmod u+x catkin_ws/src/beginnertutorials/controlnode2.py

import rospy
import sys
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


## Global variables ########
rospy.init_node('rotatingturtle', anonymous=True)
pub = rospy.Publisher("turtle3/cmd_vel", Twist, queue_size=10)
pose = Pose()
rate=rospy.Rate(10)

velmsg = Twist()
velmsg.linear.x = 0.0
velmsg.linear.y = 0
velmsg.linear.z = 0
velmsg.angular.x = 0
velmsg.angular.y = 0
velmsg.angular.z = 0.0

incremental = 0.015

## Getter and setters #######

def getPoseX():
        return pose.x
def setPoseX(data):
        pose.x = data
def getPoseY():
	return pose.y
def setPoseY(data):
	pose.y = data



### Unique Method ###

def Turtle2Motion():
	velmsg.angular.z = -1
	while not rospy.is_shutdown(): # Or while true

		if(getPoseY() <= 0.36): # Round --1
			velmsg.linear.x = 1.0
			setPoseY(getPoseY()+incremental)
		elif(getPoseY()>0.36 and getPoseY()<=0.85): # Round --2
			velmsg.linear.x = 1.6
			setPoseY(getPoseY()+incremental)
		elif(getPoseY()>0.85 and getPoseY() <=1.30): # Round --3
			velmsg.linear.x = 2.2
			setPoseY(getPoseY()+incremental)
		elif(getPoseY()>1.3 and getPoseY() <=1.78): # Round --4
			velmsg.linear.x = 2.8
			setPoseY(getPoseY()+incremental)
		elif(getPoseY()>1.78 and getPoseY() <=2.24): # Round --5
			velmsg.linear.x = 3.4
			setPoseY(getPoseY()+incremental)
		else:
			break ## STOP

		pub.publish(velmsg)
		rate.sleep()

#################################### Main Below


if __name__ == "__main__":
	try:
        	Turtle2Motion()
    	except rospy.ROSInterruptException:
		pass
        
