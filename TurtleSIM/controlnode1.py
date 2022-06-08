#!/usr/bin/env python
#Source Code for Turtle 1
#chmod u+x catkin_ws/src/beginnertutorials/controlnode1.py

import rospy
import sys
import math
import time
from geometry_msgs.msg import Twist


## Global variables #
rospy.init_node('movingturtle', anonymous=True)
pub = rospy.Publisher("turtle2/cmd_vel", Twist, queue_size=10)
rate=rospy.Rate(10)
velmsg = Twist()

velmsg.linear.x = 1
velmsg.linear.y = 0
velmsg.linear.z = 0
velmsg.angular.x = 0
velmsg.angular.y = 0
velmsg.angular.z = 0.0

#################################### Rotate Method
# Turtles should face the direction they go.


def rotateRobot(angle, clockwise): 
	angular_speed  = 15 * (math.pi/180.0)
	relative_angle = angle * (math.pi/180.0)
	velmsg.linear.x = 0
	velmsg.angular.z = angular_speed * clockwise


	t0 = rospy.Time.now().to_sec()
	current_angle = 0
	while current_angle <= relative_angle:
		pub.publish(velmsg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed * (t1-t0)
		rate.sleep()
	velmsg.linear.x = 0.0
	velmsg.angular.z = 0.0
	pub.publish(velmsg)
	

#################################### Move Distance Method
# I will use this method many times for each motion

def moveDistance(goal_distance):
	t0 = rospy.Time.now().to_sec()
	current_distance = 0
	while current_distance <= goal_distance:
		pub.publish(velmsg)
		t1 = rospy.Time.now().to_sec()
		current_distance = velmsg.linear.x * (t1-t0)
		rate.sleep()

	velmsg.linear.x = 0.0
	current_distance = 0.0
	pub.publish(velmsg) #STOP


####################################

def Turtle1Motion(initialDirection, round2, round3):
		Distance = 1.0
		DownDistance = 0.2
		#############################################
		if initialDirection == 'Right':
			moveDistance(Distance)
			rotateRobot(88,-1) # ROTATE
			velmsg.linear.x = 1
			moveDistance(DownDistance)
			rotateRobot(87.5,-1) # ROTATE
			velmsg.linear.x = 1
			moveDistance(Distance) 

			if round2 == 'Right':
				Distance+=1 #Right after Right
				rotateRobot(87.2,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance+0.1)
				rotateRobot(87.2,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)
				rotateRobot(88,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance+0.1)
				rotateRobot(87.5,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)

				if round3 == 'Right': #Right-Right-Right Case
					Distance+=1 #Right after Right
					rotateRobot(87.2,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.2)
					rotateRobot(87.2,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
					rotateRobot(88,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.2)
					rotateRobot(87.5,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)

				elif round3 == 'Left':
					velmsg.linear.x = 1
					Distance *=2
					moveDistance(Distance) 
					# it doubled its distance
					rotateRobot(88,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance)
					rotateRobot(87.5,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
				else:
					rospy.loginfo("This program does not support vertical directions.")
						
			elif round2 == 'Left':
				velmsg.linear.x = 1
				Distance*=2
				moveDistance(Distance) #it doubled its distance
				rotateRobot(88,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance)
				rotateRobot(87.5,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)
				if round3 == 'Right':
					velmsg.linear.x = 1
					Distance*=2
					moveDistance(Distance)
					rotateRobot(88,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance)
					rotateRobot(87.5,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)	
				elif round3 == 'Left':
					Distance+=1 #Left after left
					rotateRobot(87.2,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.1)
					rotateRobot(87.2,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
					rotateRobot(88,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.1)
					rotateRobot(87.2,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
				else:
					rospy.loginfo("This program does not support vertical directions.")
			else:
				rospy.loginfo("This program does not support vertical directions.")
						

		################################################
		elif initialDirection == 'Left':
			rotateRobot(181.5,1) # ROTATE to Left (Initial)
			velmsg.linear.x = 1
			moveDistance(Distance)
			rotateRobot(88,1) # ROTATE
			velmsg.linear.x = 1
			moveDistance(DownDistance)
			rotateRobot(87.5,1) # ROTATE
			velmsg.linear.x = 1
			moveDistance(Distance) 
			if round2 == 'Right':
				velmsg.linear.x = 1
				Distance*=2
				moveDistance(Distance) #it doubled its distance
				rotateRobot(88,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance)
				rotateRobot(87.6,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)
				if round3 == 'Right':
					Distance+=1 #Right after Right
					rotateRobot(87.2,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.1)
					rotateRobot(87.2,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
					rotateRobot(88,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.1)
					rotateRobot(87.5,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
				elif round3 == 'Left':
					velmsg.linear.x = 1
					Distance*=2
					moveDistance(Distance)
					rotateRobot(88,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance)
					rotateRobot(87.6,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
				else:
					rospy.loginfo("This program does not support vertical directions.")
			elif round2 == 'Left':
				Distance+=1 #Left after Left
				rotateRobot(87.2,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance+0.1)
				rotateRobot(87.2,-1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)
				rotateRobot(88,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(DownDistance+0.1)
				rotateRobot(87.5,1) # ROTATE
				velmsg.linear.x = 1
				moveDistance(Distance)
				if round3 == 'Right':
					velmsg.linear.x = 1
					Distance *=2
					moveDistance(Distance) 
					# it doubled its distance
					rotateRobot(88,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance)
					rotateRobot(87.5,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)	

				elif round3 == 'Left':
					Distance+=1 #Right after Right
					rotateRobot(87.2,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.2)
					rotateRobot(87.2,-1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
					rotateRobot(88,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(DownDistance+0.2)
					rotateRobot(87.5,1) # ROTATE
					velmsg.linear.x = 1
					moveDistance(Distance)
				else:
					rospy.loginfo("This program does not support vertical directions.")
			else:
				rospy.loginfo("This program does not support vertical directions.")

		else:
			rospy.loginfo("This program does not support vertical directions.")

	

####################################


if __name__ == "__main__":
	try:
        	Turtle1Motion("Right","Right","Left") 
## We should give only Right or Left parameters. Otherwise it gives an exception
    	except rospy.ROSInterruptException:
		pass
        
