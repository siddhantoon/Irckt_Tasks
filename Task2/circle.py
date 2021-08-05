#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

rospy.set_param('/use_sim_time',True)

# At angular velocity of PI, rotation for time 0.95 seconds results in 90 degree angle.

def automate():
	rospy.init_node('Automatic_Controller')
	rate=rospy.Rate(10)
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=2)

	while not rospy.is_shutdown():
		# Circle constant angular and linear velocity
		move_cmd= Twist()

		move_cmd.angular.z=1
		move_cmd.linear.x=1
		pub.publish(move_cmd)
		rate.sleep()

if __name__ == "__main__":
	try:
		automate()
	except rospy.ROSInterruptException:
		pass