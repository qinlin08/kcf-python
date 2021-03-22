# encoding=utf-8
import numpy as np
import cv2
import sys
from time import time
import os

import kcftracker

selectingObject = False
initTracking = False
onTracking = False
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0

inteval = 1
duration = 0.01


# mouse callback function
def draw_boundingbox(event, x, y, flags, param):
    global selectingObject, initTracking, onTracking, ix, iy, cx, cy, w, h

    if event == cv2.EVENT_LBUTTONDOWN:
        selectingObject = True
        onTracking = False
        ix, iy = x, y
        cx, cy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        cx, cy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        selectingObject = False
        if (abs(x - ix) > 10 and abs(y - iy) > 10):
            w, h = abs(x - ix), abs(y - iy)
            ix, iy = min(x, ix), min(y, iy)
            initTracking = True
        else:
            onTracking = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        onTracking = False
        if (w > 0):
            ix, iy = x - w / 2, y - h / 2
            initTracking = True


if __name__ == '__main__':
    tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
    path = './Basketball/img'
    path_list = os.listdir(path)
    path_list.sort()
    i = 0

    _roi = [0., 0., 0., 0.]

    print(_roi[0])

    for filename in path_list:
        print(filename)
        oimg = cv2.imread(path + "/" + filename)
        if i == 0:
            tracker.init([200, 200, 50, 50], oimg)
        else:
            boundingbox = tracker.update(oimg)
            boundingbox = map(int, boundingbox)
            boundingbox = list(boundingbox)

            cv2.rectangle(oimg, (boundingbox[0], boundingbox[1]), (boundingbox[0] +
                                                                   boundingbox[2], boundingbox[1] + boundingbox[3]),
                          (0, 255, 255), 1)
            #tpath1 = str(i + 100000) + 'result.jpg'
            #cv2.imwrite(tpath1, oimg)
            cv2.imshow('traking', oimg)
            cv2.waitKey(20)
        i = i + 1