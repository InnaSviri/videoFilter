import errno
import os

import cv2

from pascal_voc_writer import Writer

from inOut import InputReader


class OutputFormer:
    __output_num = 0

    def __init__(self):
        global __output_num
        self.__increase_outnum()
        self.path_to_out = InputReader.args["output"] + "/out_" + str(__output_num)
        self.make_out_directory()

        self.writer = None
        if InputReader.args["video"]:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            self.writer = cv2.VideoWriter(self.path_to_out, fourcc, 30, (400,400), True)

    def add_pict(self, img, picks, frame_num):
        _path_to_img = self.path_to_out + "/IMG_" + str(frame_num) + ".jpg"
        _path_to_xml = self.path_to_out + "/IMG_" + str(frame_num) + ".xml"

        cv2.imwrite(_path_to_img, img)
        writer = Writer(_path_to_img, img.shape[1], img.shape[0])
        for (xA, yA, xB, yB) in picks:
            writer.addObject('pedestrian', xA, yA, xB, yB)
        writer.save(_path_to_xml)

    def close(self, fps):
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        if self.writer is not None:
            self.writer.release()

    def __increase_outnum(self):
        global __output_num
        __output_num =+ 1

    def make_out_directory(self):
       try:
           if not os.path.exists(self.path_to_out):
               os.mkdir(self.path_to_out)
       except OSError:
           print("Создать директорию %s не удалось" % self.path_to_out)
       else:
           print("Успешно создана директория %s " % self.path_to_out)