import cv2
import imutils
import numpy as np
from imutils.object_detection import non_max_suppression


# initialize the HOG descriptor/person detector
from inOut import InputReader

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(image, params):
    if InputReader.args["prototxt"] != None and InputReader.args["model"] != None:
        net = cv2.dnn.readNetFromCaffe(InputReader.args["prototxt"], InputReader.args["model"])
        pick  = __caffe_detector(image, net, params)
    else:
        pick = __default_detector(image, params)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    return pick, image


def __default_detector(image, params):
    # resize image to have a maximum width of 400 pixels
    image = imutils.resize(image, width=min(400, image.shape[1]))
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=params.winStride,
                                            padding=params.padding, scale=params.scale)

    # TODO add confidence filter

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    return pick

def __caffe_detector(img, net, params):
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    img = imutils.resize(img, width=500)
    (H, W) = img.shape[:2]

    blob = cv2.dnn.blobFromImage(img, 0.007843, (W, H), 127.5)
    net.setInput(blob)
    detections = net.forward()

    boxes = []
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated
        # with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by requiring a minimum
        # confidence
        if confidence > params.confidence:
            # extract the index of the class label from the
            # detections list
            idx = int(detections[0, 0, i, 1])

            # if the class label is not a person, ignore it
            if CLASSES[idx] != "person":
                continue
            # compute the (x, y)-coordinates of the bounding box
            # for the object
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")
            boxes.append([startX, startY, endX, endY])

    return boxes