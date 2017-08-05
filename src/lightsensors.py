#!/usr/bin/env python
#encoding: utf8
import sys, rospy
from piavatar_ros.msg import LightSensorValues

def get_freq():
    f = rospy.get_param('lightsensors_freq',10)
    try:
        if f <= 0.0:
            raise Exception()
    except:
        rospy.logger("value error: lightsensors_freq")
        sys.exit(1)

    return f
        
if __name__ == '__main__':
    devfile = '/dev/rtlightsensor0'
    rospy.init_node('lightsensors')
    pub = rospy.Publisher('lightsensors', LightSensorValues, queue_size=1)

    freq = get_freq()
    rate = rospy.Rate(freq)
    while not rospy.is_shutdown():
        try:
            with open(devfile, 'r') as f:
                data = f.readline().split()
                data = [ int(e) for e in data ]
                d = LightSensorValues()
                d.right_forward = data[0]
                d.right_side = data[1]
                d.left_side  = data[2]
                d.left_forward = data[3]
                d.sum_all = sum(data)
                d.sum_forward = data[0] + data[3]
                pub.publish(d)
        except IOError:
            rospy.logerr("cannot write to " + devfile)

        f = get_freq()
        if f != freq:
            freq = f
            rate = rospy.Rate(freq)

        rate.sleep()
 
