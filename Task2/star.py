#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

rospy.set_param('/use_sim_time',True)

# At angular velocity of PI, rotation for time 0.95 seconds results in 90 degree angle.

def automate():
	rospy.init_node('Star')
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=2)

# ang z +ve left turn lin x +ve forward 
	while not rospy.is_shutdown():
		rospy.sleep(1.0)
		
		move_cmd= Twist()
		# Turn 144 degrees left
		move_cmd.angular.z=PI
		pub.publish(move_cmd)
		rospy.sleep(1.5344)
		
		# Stop
		move_cmd.angular.z=0.0
		pub.publish(move_cmd)
		rospy.sleep(1.0)
		
		# forward
		move_cmd.linear.x=0.5
		pub.publish(move_cmd)
		rospy.sleep(2.0)
		
		# Stop
		move_cmd.linear.x=0
		pub.publish(move_cmd)

if __name__ == "__main__":
	try:
		automate()
	except rospy.ROSInterruptException:
		pass