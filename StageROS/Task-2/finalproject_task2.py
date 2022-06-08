#!/usr/bin/env python
#18070006024 Final Project Task 2
#chmod u+x catkin_ws/src/beginner_msgsrv/finalproject_task2.py

import rospy
import sys
import tf
from geometry_msgs.msg import Pose2D
from math import pow, atan2, sqrt
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from beginner_msgsrv.srv import*

nodeid = str(sys.argv[1])
nodename = "robot_" + nodeid

roll = pitch = yaw = 0

class Robot:
    def __init__(self):
        rospy.init_node('moving_node', anonymous=True)
        self.pub = rospy.Publisher(nodename+"/cmd_vel", Twist, queue_size=10)
	self.sub = rospy.Subscriber(nodename+"/odom", Odometry, self.update_pose)
        self.pose = Pose2D()
        self.rate=rospy.Rate(10)
        
##########################
    def update_pose(self,msg): #Our update pose is now feeding with Odom
	global roll, pitch, yaw
        self.pose.x = msg.pose.pose.position.x
	self.pose.y = msg.pose.pose.position.y
	q = msg.pose.pose.orientation
	q_list = [q.x, q.y, q.z, q.w]
	(roll, pitch, yaw) = tf.transformations.euler_from_quaternion(q_list)
	self.pose.theta = yaw
##########################




##########################  Distance Service
    def euclidean_distance(self, goal_pose):
	rospy.wait_for_service("euclideandist")
	try:
		e_dist = rospy.ServiceProxy("euclideandist", EuclideanDistance)
		response = e_dist(goal_pose.y, goal_pose.x, self.pose.x, self.pose.y)
		return response.result
	except Exception as e:
		print(e)
########################## 
    def linear_vel(self,goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)
        
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y-self.pose.y, goal_pose.x - self.pose.x) 
        
    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose)-self.pose.theta)
########################## 
    def move2goal(self):
        goalpose = Pose2D()
	
	#Goal Positions for each robot (StageROS)
	#Substracting the initial location of robot from the goalpose
	# Way 1-2
	
	if nodeid == '0': #Initial Location: 0,0 : No concrete substraction
        	goalpose.x = rospy.get_param("goalposex_r1") - 0
        	goalpose.y = rospy.get_param("goalposey_r1") - 0
	elif nodeid == '1': #Initial location -1 , -1
		goalpose.x = rospy.get_param("goalposex_r2") - (-1)
        	goalpose.y = rospy.get_param("goalposey_r2") - (-1)
	
	''' 
	#At Way-3 (For Gazebo), no rospy.get_param() needed, so I will give parameters by my own:
	if nodeid == '0': 
        	goalpose.x = 2 - 0
        	goalpose.y = 2 - 0
	elif nodeid == '1': 
		goalpose.x = -4 - (-1)
		goalpose.y = -4 - (-1)
	#Again substract initial poses
	'''


        tolerance = 0.01
        vel_msg = Twist()
        
        while self.euclidean_distance(goalpose) >= tolerance:
            vel_msg.linear.x = self.linear_vel(goalpose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goalpose)
            self.pub.publish(vel_msg)
            self.rate.sleep()
            
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.0
        self.pub.publish(vel_msg)
########################## 

if __name__ == "__main__":
	try:
        	x = Robot()
        	x.move2goal()
    	except Exception as e:
		print(e)
        
