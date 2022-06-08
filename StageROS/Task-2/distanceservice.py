#!/usr/bin/env python
#Task 2
# movetogoal Service Node

import rospy
from math import sqrt
from beginner_msgsrv.srv import EuclideanDistance, EuclideanDistanceResponse
        
def euclidean_distance(req):
	return EuclideanDistanceResponse(sqrt(pow((req.goalpose_x-req.selfpose_y), 2.0) + pow((req.goalpose_y-req.selfpose_y), 2.0)))
	
def movetogoal_Server():
	rospy.init_node("euclidean_distance_server")
	s = rospy.Service('euclideandist', EuclideanDistance, euclidean_distance)
	rospy.spin()

if __name__ == "__main__":
	movetogoal_Server()
