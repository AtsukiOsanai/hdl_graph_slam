#!/usr/bin/python
# SPDX-License-Identifier: BSD-2-Clause

import tf2_ros
import rospy
from geometry_msgs.msg import *


def main():
    rospy.init_node('sensor2base_publisher')

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    # broadcaster = tf2_ros.TransformBroadcaster()
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)

    base_frame = rospy.get_param('base_frame', 'base_link')
    sensor_frame = rospy.get_param('sensor_frame', 'velodyne')
    mapping_base_frame = rospy.get_param('mapping_base_frame', 'mapping_base_link')

    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown():
        try:
            transform = buffer.lookup_transform(base_frame, sensor_frame, rospy.Time(0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        static_transformStamped = geometry_msgs.msg.TransformStamped()
        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = mapping_base_frame
        static_transformStamped.child_frame_id = sensor_frame
        static_transformStamped.transform = transform.transform

        broadcaster.sendTransform(static_transformStamped)
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except:
        print 'shutdown'

