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
import PX4MavCtrlV4 as PX4MavCtrl
import ScreenCapApiV4 as sca

# Function to calculate the location and radius of red ball
def calc_centroid(img):
    """Get the centroid and area of green in the image"""
    low_range = np.array([0,0,80])
    high_range = np.array([100,100,255])
    th = cv2.inRange(img, low_range, high_range)
    dilated = cv2.dilate(th, cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    cv2.imshow("dilated", dilated)
    cv2.waitKey(1)

    M = cv2.moments(dilated, binaryImage=True)
    if M["m00"] >= min_prop*width*height:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return [cx, cy, M["m00"]]
    else:
        return [-1, -1, -1]

# Function to obtain velocity commands for Pixhawk 
# according to the image processing results
def controller(p_i):
    # if the object is not in the image, search in clockwise
    if p_i[0] < 0 or p_i[1] < 0:
        return [0, 0, 0, 1]

    # found
    ex = p_i[0] - width / 2
    ey = p_i[1] - height / 2

    vx = 2 if p_i[2] < max_prop*width*height else 0
    vy = 0
    vz = K_z * ey
    yawrate = K_yawrate * ex
    
    # return forward, rightward, downward, and rightward-yaw 
    # velocity control sigals
    return [vx, vy, vz, yawrate]

# Process image to obtain vehicle velocity control command
def procssImage():
    img_rgba=sca.getCVImg(ImgInfo1)
    img_bgr = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
    img_bgr = cv2.resize(img_bgr, (width, height))
    p_i = calc_centroid(img_bgr) 
    ctrl = controller(p_i) 
    return ctrl

# saturation function to limit the maximum velocity
def sat(inPwm,thres=1):
    outPwm= inPwm
    for i in range(len(inPwm)):
        if inPwm[i]>thres:
            outPwm[i] = thres
        elif inPwm[i]<-thres:
            outPwm[i] = -thres
    return outPwm

# Create MAVLink control API instance
mav = PX4MavCtrl.PX4MavCtrler(20100)
# Init MAVLink data receiving loop
mav.InitMavLoop()

isEmptyData = False
lastTime = time.time()
startTime = time.time()
# time interval of the timer
timeInterval = 0.01 #here is 0.01s (100Hz)
flag = 0

# parameters
width = 720
height = 405
channel = 4
min_prop = 0.000001
max_prop = 0.3
K_z = 0.003 * 640 / height
K_yawrate = 0.005 * 480 / width

# send command to all RflySim3D windows to switch to the blank grass scene 
# by default, there are two windows, the first is front camera 
# for vison control, and the second window for observation
mav.sendUE4Cmd(b'RflyChangeMapbyName VisionRingBlank')
time.sleep(1)

# create a ball, set its position and altitude, use the default red color
mav.sendUE4Pos(100,152,0,[3,0,-2],[0,0,0])
time.sleep(0.5)

# Change the target vehicle to copterID=1's vehicle
mav.sendUE4Cmd(b'RflyChangeViewKeyCmd B 1',0)
time.sleep(0.5)  
# Switch its viewpoint to oboard #1 (front camera view)
mav.sendUE4Cmd(b'RflyChangeViewKeyCmd V 1',0)
time.sleep(0.5)
# move the camera to the position [0.3,0,0.05] related to the body
mav.sendUE4Cmd(b'RflyCameraPosAng 0.3 0 0.05 0 0 0',0)
time.sleep(0.5)    
# set the RflySim3D window size to 720x405
mav.sendUE4Cmd(b'r.setres 720x405w',0)   
time.sleep(2)

window_hwnds = sca.getWndHandls()
Wd01 = window_hwnds[0]
hasFoundWd = False
for hwd in window_hwnds:
    info = sca.getHwndInfo(hwd)
    if info.width == 720:
        Wd01 = hwd
        hasFoundWd = True
        window_hwnds.remove(hwd)
        break

# if no window is found, throw an error
if not hasFoundWd:
    print("The first RflySim3D window does not response the command, please close all apps and try again.")
    mav.stopRun()
    sys.exit(1)    
else:
    print("The first RflySim3D window is found with desired size.")
    
ImgInfo1 = sca.getHwndInfo(Wd01)
    
ctrlLast = [0,0,0,0]
while True:
    lastTime = lastTime + timeInterval
    sleepTime = lastTime - time.time()
    if sleepTime > 0:
        time.sleep(sleepTime)
    else:
        lastTime = time.time()
    # The following code will be executed 100Hz (0.01s)

    if time.time() - startTime > 5 and flag == 0:
        # The following code will be executed at 5s
        print("5s, Arm the drone")
        mav.initOffboard()
        flag = 1
        mav.SendMavArm(True) # Arm the drone
        print("Arm the drone!, and fly to NED 0,0,-5")
        mav.SendPosNED(0, 0, -5, 0) # Fly to target position [0, 0, -5], i.e., take off to 5m

    if time.time() - startTime > 15 and flag == 1:
        flag = 2
         # The following code will be executed at 15s
        mav.SendPosNED(-30,-5, -5, 0)  # Fly to target position [-30,-5, -5]
        print("15s, fly to pos: -30,-5, -5")

    if time.time() - startTime > 25 and flag == 2:
        flag = 3
        print("25s, start to shoot the ball.")

    if time.time() - startTime > 25 and flag == 3:
        ctrlNow = procssImage()
        ctrl = sat(ctrlNow,5)
        # add a inertial component here to restrain the speed variation rate
        if ctrl[0]-ctrlLast[0] > 0.5:
            ctrl[0]=ctrlLast[0]+0.05
        elif ctrl[0]-ctrlLast[0] < -0.5:
            ctrl[0]=ctrlLast[0]-0.05
        if ctrl[1]-ctrlLast[1] > 0.5:
            ctrl[1]=ctrlLast[1]+0.05
        elif ctrl[1]-ctrlLast[1] < -0.5:
            ctrl[1]=ctrlLast[1]-0.05        
        ctrlLast = ctrl
        # if control signals is obtained, send to Pixhawk
        if not isEmptyData:
            mav.SendVelFRD(ctrl[0], ctrl[1], ctrl[2], ctrl[3])