import cv2
import os
import time
import datetime
import threading
import imutils

Video_FPS = 20
Video_Resolution = (1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#fourcc = cv2.VideoWriter_fourcc(*'H264')
#fourcc = cv2.VideoWriter_fourcc(*'mp4v') #.avi or .mp4
#fourcc = cv2.VideoWriter_fourcc(*'XVID') #.avi or .mp4
#fourcc = cv2.VideoWriter_fourcc(*'MJPG') #.avi
#fourcc = cv2.VideoWriter_fourcc(*'DIVX') #.avi or .mp4
#fourcc = cv2.VideoWriter_fourcc(*'X264') #.mp4

######Multithread######
######################################
class WebcamVideoStream:
    def __init__(self, camera_name, video_path, motion):
        print("thread init - " + camera_name)
        self.title = str(camera_name)
        self.source = str(video_path)
        self.motion = int(motion)
        self.stream = cv2.VideoCapture(self.source)
        self.grabbed, self.frame = self.stream.read()
        self.buffer_frame = []
        self.reconnect_count = 0
        self.started = False
        self.read_lock = threading.Lock()
        self.refresh_time = datetime.datetime.now().strftime("%H;%M;%S")
        self.motion_refresh = 0
        self.previous_frame = None
        self.out = None
        self.stamp_time = datetime.datetime.now().strftime("%Y-%m-%d_%H")
        print(camera_name)
        print(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH), self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT),
              self.stream.get(cv2.CAP_PROP_FPS))

    def start(self):
        if self.started:
            print(self.title + " already started!!")
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while (self.started is True):
            self.grabbed, self.frame = self.stream.read()
            self.read_lock.acquire()
            if self.grabbed is True:
                #Video_Resolution = (self.frame.shape[1], self.frame.shape[0])
                if len(self.buffer_frame) > 10: self.buffer_frame.pop(0) # keep 10 buffer frame
                self.buffer_frame.append(self.frame)
                
                # create video file
                CurrentDate = datetime.datetime.now()
                FolderDate = "./record/" + CurrentDate.strftime("%Y-%m-%d") + "/" + self.title
                if not os.path.exists(FolderDate): os.makedirs(FolderDate)
                if self.out is None or self.out.isOpened() is False:
                    Stamp_Time = self.title + CurrentDate.strftime("~%Y-%m-%d_%H;%M;%S") + ".mp4"
                    File_Name = FolderDate + "/" + Stamp_Time
                    self.out = cv2.VideoWriter(File_Name, fourcc, Video_FPS, Video_Resolution)
                    print("Start video file ", File_Name)
                else:
                    if self.stamp_time != CurrentDate.strftime("%Y-%m-%d_%H"):
                        self.stamp_time = CurrentDate.strftime("%Y-%m-%d_%H")
                        Stamp_Time = self.title + CurrentDate.strftime("~%Y-%m-%d_%H;%M;%S") + ".mp4"
                        File_Name = FolderDate + "/" + Stamp_Time
                        if self.out.isOpened() is True:
                            self.out.release()
                            self.out = cv2.VideoWriter(File_Name, fourcc, Video_FPS, Video_Resolution)
                            print("New video file ", File_Name)

                # motion detection
                resize_frame = cv2.resize(self.frame, Video_Resolution, interpolation=cv2.INTER_AREA)
                gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                if self.previous_frame is None: self.previous_frame = gray.copy()
                elif self.motion_refresh >= 60:
                    self.motion_refresh = 0
                    self.previous_frame = gray.copy()
                frameDelta = cv2.absdiff(self.previous_frame, gray)
                thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                motion = False
                for c in cnts:
                    # if the contour is too small, ignore it
                    if cv2.contourArea(c) < self.motion: continue
                    motion = True
                    break
                if motion is True:
                    current_time = CurrentDate.strftime("%H;%M;%S")
                    if self.refresh_time != current_time:
                        self.refresh_time = current_time
                        self.motion_refresh += 1
                    save_image = resize_frame.copy()
                    if self.out.isOpened() is True: self.out.write(save_image)
                time.sleep(0.03)
            self.read_lock.release()
            
            # reconnect camera
            if self.grabbed is False:
                self.stream.release()
                print(self.title + " reconnecting..." + str(self.reconnect_count))
                self.stream = cv2.VideoCapture(self.source)
                if self.stream.isOpened():
                    self.reconnect_count = 0
                    print(self.title + " is connected")
                else:
                    self.reconnect_count += 1
                    if self.reconnect_count > 5:
                        pass
#                        self.stream.release()
#                        self.started = False
#                        cv2.destroyAllWindows()

        if self.out is not None:
            if self.out.isOpened() is True:
                self.out.release()
                print("Close video file")
        if self.stream.isOpened():
            print(self.title + " thread release")
            self.stream.release()
            self.started = False
            cv2.destroyAllWindows()

    def read(self):
        self.read_lock.acquire()
        grabbed = self.grabbed
        started = self.started
        title = self.title
        buffer_frame = self.buffer_frame.copy()
        if grabbed: frame = self.frame.copy()
        else: frame = None
        self.read_lock.release()
        return grabbed, frame, buffer_frame, started, title
    
    def stop(self):
        self.started = False
######################################