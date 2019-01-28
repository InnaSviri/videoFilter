import cv2
import glob
import os

import imutils

from src.detection import people_detector
from src.inOut.InputReader import InputReader

CONFIG_PATH = 'C:/Users/User/PycharmProjects/videoFilter/resources'

def create_inputs():
    global inputs
    inputs = [InputReader(filename) for filename in glob.glob(os.path.join(CONFIG_PATH, '*.txt'))]

def get_one_decision(params):

    # loop over the frames from the video stream
    while (vs.isOpened()):
        # grab the frame from the video stream
        ret, frame = vs.read()

        if ret:
            # and resize it to have a maximum width of 400 pixels
            frame = imutils.resize(frame, width=min(400, frame.shape[1]))
            picks, image = people_detector.detect(frame, params)


            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break



create_inputs()
vs, fps = InputReader.get_video_stream()


