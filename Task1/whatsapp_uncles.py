#!/usr/bin/env python

import rospy
from std_msgs.msg import String


# Subscribe to Fake_News
def share_whatsapp():
    rospy.init_node('Whatsapp_Uncles')
    rospy.Subscriber('Fake_News',String,watch)
    rospy.spin()

def watch(data):
    fake=str(data.data)
    fake=fake[-6:-1]
    fake_news='I saw a whatsapp forward I will share this without rechecking : ' + fake
    print(fake_news)

    
if __name__ == '__main__':
    try:
        share_whatsapp()
    except rospy.ROSInterruptException:
        pass