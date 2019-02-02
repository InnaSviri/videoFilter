import argparse
import cv2
import time
import pandas as pd

from imutils.video import FPS

from src.detection.Params import Params

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	            help="path to input video file")
ap.add_argument("-v", "--video", type=bool,
                help="whether output video is necessary")
ap.add_argument("-o", "--output", type=str,
                help="path to output ")
args = vars(ap.parse_args())



class InputReader:

    def __init__(self, params_file_path):
        self.params_file = open(params_file_path, 'r')
        self.params = Params(self.params_file)

    def get_video_stream(self):
        print("[INFO] opening video file...")
        vs = cv2.VideoCapture(args["input"])
        # Check if camera opened successfully
        if (vs.isOpened() == False):
            print("Error opening video stream or file")

        fps = FPS().start()
        return vs, fps