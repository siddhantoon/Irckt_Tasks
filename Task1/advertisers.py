#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import String

# publish money
def send_money():
    #send money to do advertisements rather than News on TV News
    advertiser=rospy.Publisher('Money',String,queue_size=1)
    rospy.init_node('Advertisers')
    rate=rospy.Rate(0.2) #once every 5 seconds

    while not rospy.is_shutdown():
        money='This is ' + str(1000*random.randint(1,7)) + ' Rupees for you to Advertise my product. ;) '

        advertiser.publish(money)
        rate.sleep()


if __name__ == '__main__':
    try:
        send_money()
    except rospy.ROSInterruptException:
        pass