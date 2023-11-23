# nvr_thread
4-channel NVR to record video on motion detect (Python).

# Program features
Python implementation to stream camera feed from OpenCV videoCapture via RTSP using multithreading in which to enhance video streaming concurrently and reduce latency during streaming.

Motion detected and save video files hourly the "record" folder.

Can set the sensitivity of minimum motion area

# Installation

pip install imutils

# Requirement
Python 3.x

Opencv 3.x or above ( pip install opencv-python )

# Usage and code setting

Keep 30 days or can edit from program (eg: Keep_Data = 30) on nvr_thread.py line code 12

Change NVR display resolution (eg: Display_Resolution = (width, height)) on nvr_thread.py line code 13

Change motion area detection (pixels) from program (eg: Motion_Area = 10000) on nvr_thread.py line code 14

Change IP camera link (eg: Video_Path_1 = "rtsp://admin:sl888888@192.168.2.85") on nvr_thread.py line code 15 to 18

Change record video frame (eg: Video_FPS = 20) on camera_thread.py line code 8

Change record video resolution (eg: Video_Resolution = (width, height)) on camera_thread.py line code 9

Can change the fourcc video codec on camera_thread.py line code 10 and currently using mp4v

# Run program

python motion_detector.py

# Keyboard function:

ESC to quit the program

The video files are stored at inside the record folder
