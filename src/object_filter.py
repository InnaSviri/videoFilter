import cv2
import glob
import os

import imutils

from inOut import OutputFormer
from src.detection import people_detector
from src.inOut.InputReader import InputReader

CONFIG_PATH = 'C:/Users/User/PycharmProjects/videoFilter/resources'



def get_one_decision(inp):
    vs, fps = inp.get_video_stream()
    output = OutputFormer.OutputFormer()
    # loop over the frames from the video stream
    i = 0
    while (vs.isOpened()):
        # grab the frame from the video stream
        ret, frame = vs.read()

        if ret:
            picks, image = people_detector.detect(frame, inp.params)
            if len(picks) != 0: output.add_pict(image, picks, i)
            del image

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

        if output.writer is not None:
            output.writer.write(frame)
        i += 1
        fps.update()
        del frame

    vs.release()
    cv2.destroyAllWindows()


inputs = [InputReader(filename) for filename in glob.glob(os.path.join(CONFIG_PATH, '*.txt'))]
for inp in inputs:
    get_one_decision(inp)


