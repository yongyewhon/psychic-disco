# import the necessary packages
import imutils
import numpy as np
import argparse
import time
import datetime
import cv2
import os
import shutil
import camera_thread

Keep_Data = 30 #keep 30 days record
Display_Resolution = (800, 600)
Motion_Area = 10000
Video_Path_1 = "rtsp://admin:sl888888@192.168.2.85"
Video_Path_2 = "rtsp://admin:sl888888@192.168.2.86"
Video_Path_3 = "rtsp://admin:sl888888@192.168.2.87"
Video_Path_4 = "rtsp://admin:sl888888@192.168.2.88"
(Display_W, Display_H) = (int(Display_Resolution[0]/2), int(Display_Resolution[1]/2))
frame_cam1 = np.zeros((Display_H, Display_W, 3), np.uint8)
frame_cam2 = np.zeros((Display_H, Display_W, 3), np.uint8)
frame_cam3 = np.zeros((Display_H, Display_W, 3), np.uint8)
frame_cam4 = np.zeros((Display_H, Display_W, 3), np.uint8)
Start_Program = datetime.datetime.now().strftime("%Y-%m-%d")

def Delete_old_record(day):
    today = datetime.datetime.today()
    days_ago = today - datetime.timedelta(days=Keep_Data)
    print(days_ago)
    while(True):
        for x in range(int(day)):
            try:
                day_ago = days_ago - datetime.timedelta(days=x)
                folder = day_ago.strftime("%Y-%m-%d")
                print("Delete ", folder)
                shutil.rmtree("./record/" + folder)
            except:
                print("No folder")
                continue
        break

Delete_old_record(60)
vs1 = camera_thread.WebcamVideoStream("CAM1", Video_Path_1, Motion_Area).start()
vs2 = camera_thread.WebcamVideoStream("CAM2", Video_Path_2, Motion_Area).start()
vs3 = camera_thread.WebcamVideoStream("CAM3", Video_Path_3, Motion_Area).start()
vs4 = camera_thread.WebcamVideoStream("CAM4", Video_Path_4, Motion_Area).start()
time.sleep(5.0)

run = True
while(run):
    Ret_1, Frame_1, _, Run_1, Title_1 = vs1.read()
    if Ret_1 is True:
        frame1 = cv2.resize(Frame_1, (Display_W, Display_H), interpolation=cv2.INTER_AREA)
        cv2.putText(frame1, Title_1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, Display_W/800, (255, 255, 255), 1)
    Ret_2, Frame_2, _, Run_2, Title_2 = vs2.read()
    if Ret_2 is True:
        frame2 = cv2.resize(Frame_2, (Display_W, Display_H), interpolation=cv2.INTER_AREA)
        cv2.putText(frame2, Title_2, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, Display_W/800, (255, 255, 255), 1)
    Ret_3, Frame_3, _, Run_3, Title_3 = vs3.read()
    if Ret_3 is True:
        frame3 = cv2.resize(Frame_3, (Display_W, Display_H), interpolation=cv2.INTER_AREA)
        cv2.putText(frame3, Title_3, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, Display_W/800, (255, 255, 255), 1)
    Ret_4, Frame_4, _, Run_4, Title_4 = vs4.read()
    if Ret_4 is True:
        frame4 = cv2.resize(Frame_4, (Display_W, Display_H), interpolation=cv2.INTER_AREA)
        cv2.putText(frame4, Title_4, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, Display_W/800, (255, 255, 255), 1)

    upper = cv2.hconcat([frame1, frame2])
    lower = cv2.hconcat([frame3, frame4])
    merged_frame = np.vstack((upper, lower))
    cv2.imshow("Live NVR", merged_frame)
     
    Run_Program = datetime.datetime.now().strftime("%Y-%m-%d")
    if Run_Program != Start_Program:
        Start_Program = Run_Program
        Delete_old_record(1)
        
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        vs1.stop()
        Run_1 = False
        vs2.stop()
        Run_2 = False
        vs3.stop()
        Run_3 = False
        vs4.stop()
        Run_4 = False
        break

cv2.destroyAllWindows()
print("End")
