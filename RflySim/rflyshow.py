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
        # Change the target vehicle to copterID=1's vehicle
        self.mav.sendUE4Cmd(b'RflyChangeViewKeyCmd B 1',0)
        time.sleep(0.5)
        # Switch its viewpoint to oboard #1 (front camera view)
        self.mav.sendUE4Cmd(b'RflyChangeViewKeyCmd V 1',0)
        time.sleep(0.5)
        # move the camera to the position [0.3,0,0.05] related to the body
        self.mav.sendUE4Cmd(b'RflyCameraPosAng 0.3 0 0.05 0 0 0',0)
        time.sleep(0.5)

    def draw_line(self, id, start, end):
        start = np.array([start.position[0], start.position[1], -start.position[2]])
        end = np.array([end.position[0], end.position[1], -end.position[2]])

        PosE = (start + end) / 2
        AngEuler = [0, 
                    np.arctan2(-end[2] + start[2], np.linalg.norm([end[0] - start[0], end[1] - start[1]])), 
                    np.arctan2(end[1] - start[1], end[0] - start[0])]
        Scale = [np.linalg.norm(start - end), 0.1, 0.1]
        self.mav.sendUE4PosScale(id, 207, 0, PosE, AngEuler, Scale)

    def render(self, WL, TL, init_yaw, results):
        wlid_rflyid_mp = dict()     # {unit.id: rflysim.id}
        for i in range(len(WL.units)):
            self.mav.sendUE4Pos(i, 3, 0, [WL.units[i].position[0], WL.units[i].position[1], -WL.units[i].position[2]], [0,0,init_yaw])
            wlid_rflyid_mp[WL.units[i].id] = i
        for i in range(len(TL.units)):
            self.mav.sendUE4Pos(100+i, 5, 0, [TL.units[i].position[0], TL.units[i].position[1], -TL.units[i].position[2]], [0,0,np.pi+init_yaw])
        for i in range(len(results)):
            self.draw_line(200+i, results[i][0], results[i][1])

        # episode
        