import argparse
import cv2
import time
import pandas as pd

from imutils.video import FPS, VideoStream

from src.detection.Params import Params

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=bool,
                help="whether output video is necessary")
ap.add_argument("-o", "--output", type=str,
                help="path to output ")
args = vars(ap.parse_args())


def get_video_stream():

    print("[INFO] opening video file...")
    vs = cv2.VideoCapture(args["input"])
    # Check if camera opened successfully
    if (vs.isOpened() == False):
        print("Error opening video stream or file")

    fps = FPS().start()
    return vs, fps


class InputReader:

    def __init__(self, params_file_path):
        self.params_file = pd.read_csv(params_file_path)
        self.params = Params(self.params_file)


