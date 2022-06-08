#!/usr/bin/env python
#18070006024 Final Project Task 1
#Egemen ONER
#chmod u+x catkin_ws/src/beginnertutorials/finalproject_task1.py

import rospy
import sys
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


nodeid= str(sys.argv[1])
nodename = "robot_" + nodeid

rospy.init_node("movenode", anonymous=True)
pub = rospy.Publisher(nodename+"/cmd_vel", Twist, queue_size=10)

### GLOBALS ### 
velmsg = Twist()
velmsg.linear.x = 0.5
velmsg.linear.y = 0
velmsg.linear.z = 0
velmsg.angular.x = 0
velmsg.angular.y = 0
velmsg.angular.z = 0

# Below 3 global variables are to initialized to control the rounds. 

r1_finish = False # Round 1 started as initial.
r2_finish = True # Round 2 Not started yet
r3_finish = True # Round 3 Not started yet

### ROTATE ROBOT FUNCTION #### 
ctrl_c = False 

def rotateRobot(speed, angle, clockwise, lspeed=0.0): 
	
	angular_speed  = speed * (math.pi/180.0)
	relative_angle = angle * (math.pi/180.0)
	rate=rospy.Rate(10)
	velmsg.linear.x = lspeed
	velmsg.angular.z = clockwise * abs(angular_speed)
    
    
	while not ctrl_c:
		connections = pub.get_num_connections()
		if connections > 0:
			pub.publish(velmsg)
			break
		else:
			rate.sleep()
        
        
	t0 = rospy.Time.now().to_sec()
	current_angle = 0
	
	while(current_angle < relative_angle):
		pub.publish(velmsg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed * (t1-t0)
		rate.sleep()
	
	velmsg.linear.x = 0.0
	velmsg.angular.z = 0.0
	pub.publish(velmsg)
######################### Move Distance
def moveDistance(goal_distance):
	rate=rospy.Rate(10)
	velmsg.linear.x = 1
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
#########################
# moveUntilObstacle: This function makes the robot stop if it detects an obstacle.
#########################
def moveUntilObstacle(msg):
        obstacle = False
	global r1_finish
	for i in range(len(msg.ranges)):
		if(i>=0 and i <=35) or (i>=125 and i <=142) or (i>=235 and i <=260):
			if msg.ranges[i] < 0.5:
				obstacle = True
	if not obstacle:
		velmsg.linear.x = 1
	else: # If they are nearby obstacle, they change their motion.
		velmsg.linear.x = 0.0 # Firstly, they stop their motion.
		r1_finish = True
	pub.publish(velmsg)

def moveUntilObstacle_R2(msg):
        obstacle = False
	global r2_finish
	for i in range(len(msg.ranges)):
		if(i>=0 and i <=35) or (i>=125 and i <=142) or (i>=235 and i <=260):
			if msg.ranges[i] < 0.5:
				obstacle = True
	if not obstacle:
		velmsg.linear.x = 1
	else:
		velmsg.linear.x = 0.0 
		r2_finish = True
	pub.publish(velmsg)

def moveUntilObstacle_R3(msg):
        obstacle = False
	global r3_finish
	for i in range(len(msg.ranges)):
		if(i>=0 and i <=35) or (i>=125 and i <=142) or (i>=235 and i <=260):
			if msg.ranges[i] < 0.5:
				obstacle = True
	if not obstacle:
		velmsg.linear.x = 1
	else:
		velmsg.linear.x = 0.0 
		r3_finish = True
	pub.publish(velmsg)

######################### All Three functions are same. Their only difference is they control r1_finish, r2_finish and r3_finish variables.

if __name__ == "__main__":
	try:	
################################################################ Round 1
		while not r1_finish:
			msg = rospy.wait_for_message(nodename+'/base_scan', LaserScan, timeout=5)
			moveUntilObstacle(msg) # Round 1
#Then, rotate
		if nodeid == '0':
			rotateRobot(10.0,89.45,-1.0)
			moveDistance(2)
			rotateRobot(10.0,88.7,-1,0)
		elif nodeid == '1':
			rotateRobot(10.0,89.0,1,0)
			moveDistance(2)
			rotateRobot(10.0,89.4,1,0)
################################################################ Round 2
		r2_finish = False # Set round2_finish: false and start the while loop
		while not r2_finish:
			msg = rospy.wait_for_message(nodename+'/base_scan', LaserScan, timeout=5)
			moveUntilObstacle_R2(msg) # Round 2

#Then, rotate
		if nodeid == '0':
			rotateRobot(10.0,88.6,1.0)
			moveDistance(2)
			rotateRobot(10.0,88.8,1,0)
		elif nodeid == '1':
			rotateRobot(10.0,88.6,-1,0)
			moveDistance(2)
			rotateRobot(10.0,88.8,-1,0)
################################################################ Round 3
		r3_finish = False # Set round2_finish: false and start the while loop

		while not r3_finish:
			msg = rospy.wait_for_message(nodename+'/base_scan', LaserScan, timeout=5)
			moveUntilObstacle_R3(msg) # Round 3

		#Then, rotate
		if nodeid == '0':
			rotateRobot(10.0,89.45,-1.0)
			moveDistance(2)
			rotateRobot(10.0,89,-1,0)
			moveDistance(8)
			#Lastly, they move fixed distance to come back middle
		elif nodeid == '1':
			rotateRobot(10.0,89.45,1,0)
			moveDistance(2)
			rotateRobot(10.0,89,1,0)
			moveDistance(8)
			#Lastly, they move fixed distance to come back middle
################################################################ Main end
	except rospy.ROSInterruptException:
		pass
        
