#!/usr/bin/env python3
# TODO Set the IP as a param
from __future__ import print_function, absolute_import
from drone_controller.msg import Move
from std_msgs.msg import Int8, Int16
from utility import DroneState

import sys
import copy
import rospy


class YawCorrection:

    def __init__(self):
        # Init the ROS node
        rospy.init_node('YawCorrectionNode')
        self._log("Node Initialized")      

        # On shutdown do the following 
        rospy.on_shutdown(self.stop)

        # Set the move goal
        self._yaw = 0
        self._left_right = 0
        self._front_back = 0
        self._up_down = 0

        # Param to use the corrrection or not
        self._use_yaw_correction = rospy.get_param(rospy.get_name() + '/yaw_correction', True)

        # Display the variables
        self._log(": Yaw Correction - " + str(self._use_yaw_correction))

        # Set the rate
        self.rate = 50.0
        self.dt = 1.0 / self.rate

        # Init the drone and program state
        self._quit = False

        # Holds the drone state
        self._state = DroneState.INACTIVE

        # Create the publishers and subscribers
        self.yaw_sub            = rospy.Subscriber("/uav1/input/yawcorrection", Int8, self._setYaw)
        self.move_sub           = rospy.Subscriber("/uav1/input/beforeyawcorrection/move", Move, self._setMove)
        self.move_override_sub  = rospy.Subscriber("/uav1/input/beforeyawcorrection/move_manual", Move, self._setManualMove)
        self.state_sub          = rospy.Subscriber("/uav1/input/state", Int16, self._setstate)

        self.move_pub           = rospy.Publisher("uav1/input/move", Move, queue_size=10)

    def start(self):
        self._mainloop()

    def _setstate(self, msg):
        self._state = DroneState(int(msg.data))

    def stop(self):
        self._quit = True

    def _setMove(self, msg):
        if self._state != DroneState.MANUAL:
            self._left_right    = copy.deepcopy(int(round(msg.left_right, 0)))
            self._front_back    = copy.deepcopy(int(round(msg.front_back, 0)))
            self._up_down       = copy.deepcopy(int(round(msg.up_down, 0)))
        if not self._use_yaw_correction:
            self._yaw           = copy.deepcopy(int(round(msg.yawl_yawr, 0)))

    def _setManualMove(self, msg):
        if self._state == DroneState.MANUAL:
            self._left_right    = copy.deepcopy(int(round(msg.left_right, 0)))
            self._front_back    = copy.deepcopy(int(round(msg.front_back, 0)))
            self._up_down       = copy.deepcopy(int(round(msg.up_down, 0)))
        if not self._use_yaw_correction:
            self._yaw           = copy.deepcopy(int(round(msg.yawl_yawr, 0)))

    def _setYaw(self, msg):
        if self._use_yaw_correction:
            self._yaw = copy.deepcopy(int(round(msg.data, 0)))

    def _log(self, msg):
        print(str(rospy.get_name()) + ": " + str(msg))

    def _mainloop(self):

        r = rospy.Rate(self.rate)

        while not self._quit:    
            msg_out = Move()
            msg_out.left_right  = self._left_right
            msg_out.front_back  = self._front_back
            msg_out.up_down     = self._up_down
            msg_out.yawl_yawr = self._yaw
            self.move_pub.publish(msg_out)    

            r.sleep()

if __name__ == "__main__":
    try:
        x = YawCorrection()
        x.start()
    except KeyboardInterrupt:
        print("Manually Aborted")
        x.stop()

    print("System Exiting\n")
    sys.exit(0)
