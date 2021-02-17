# import required libraries
import time
import mmap
import numpy as np
import cv2.cv2 as cv2
from pymavlink.dialects.v20 import common as mavlink2
import win32gui, win32ui, win32con
from ctypes import windll
import sys

# import RflySim APIs
import RflySim.PX4MavCtrlV4 as PX4MavCtrl

class RFly:
    def __init__(self):
        # Create MAVLink control API instance
        self.mav = PX4MavCtrl.PX4MavCtrler(20100)
        # Init MAVLink data receiving loop
        self.mav.InitMavLoop()
        # for vison control, and the second window for observation
        self.mav.sendUE4Cmd(b'RflyChangeMapbyName VisionRingBlank')
        time.sleep(1)
        # create a ball, set its position and altitude, use the default red color
        self.mav.sendUE4Pos(100,152,0,[3,0,-2],[0,0,0])
        time.sleep(0.5)
        # Change the target vehicle to copterID=1's vehicle
        self.mav.sendUE4Cmd(b'RflyChangeViewKeyCmd B 1',0)
        time.sleep(0.5)
        # Switch its viewpoint to oboard #1 (front camera view)
        self.mav.sendUE4Cmd(b'RflyChangeViewKeyCmd V 1',0)
        time.sleep(0.5)
        # move the camera to the position [0.3,0,0.05] related to the body
        self.mav.sendUE4Cmd(b'RflyCameraPosAng 0.3 0 0.05 0 0 0',0)
        time.sleep(0.5)

    def render(self, positions):
        print("positions", positions)
        for i in range(len(positions)):
            self.mav.sendUE4Pos(i, 3, 0, -positions[i], [0,0,0])
