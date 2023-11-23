# nvr_thread
4-channel NVR to record video on motion detect (Python).

# Program features
Python implementation to stream camera feed from OpenCV videoCapture via RTSP using multithreading in which to enhance video streaming concurrently and Reduce Latency during streaming.

Motion detected and save video files hourly the "record: folder.


Can set the sensitivity of minimum motion area

# Installation

pip install imutils

# Requirement
Python 3.x

Opencv 3.x or above ( pip install opencv-python )

# Usage

python motion_detector.py

Keep 30 days or can edit from program (eg: Keep_Data = 30) on nvr_thread.py line code 12.

Change NVR display resolution from program (eg: Display_Resolution = (width, height)) on nvr_thread.py line code 13

Change motion area detection (pixels) from program (eg: Motion_Area = 10000) on nvr_thread.py line code 14

Change IP camera link (eg: Video_Path_1 = "rtsp://admin:sl888888@192.168.2.85") on nvr_thread.py line code 15 to 18

The default save video format is mp4v and keep the same resolution with the streaming video

# Run program

python motion_detector.py to connect with webcam

eg: python motion_detector.py --video rtsp://admin:sl888888@10.1.1.85:554 to connect with IP camera

eg: python motion_detector.py --video rtsp://admin:sl888888@10.1.1.85:554 ----area min_area 2 --format 1 to customize the sensitivity and video format

# Keyboard function:

ESC to quit the program

The video files are stored at inside the record folder
