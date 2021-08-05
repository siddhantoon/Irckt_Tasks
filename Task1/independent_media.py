#!/usr/bin/env python

import rospy
from std_msgs.msg import String
# Subscribe to Facts
def report():
    rospy.init_node('Independent_Media')
    rospy.Subscriber('Facts',String,correctfact)
    rospy.spin()

def correctfact(data):
    news='I got these facts from reliable sources with prior investigation: ' + str(data.data)
    print(news)


if __name__ == '__main__':
    try:
        report()
    except rospy.ROSInterruptException:
        pass