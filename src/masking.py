import cv2 as cv
import numpy as np
import imutils
from threading import Thread


text_color = (255, 255, 255)
bbox_color = (36, 255, 12)
block_width = 20 # change this to virtual width. Get it with the bounding box.


def hsv2cvhsv(h, s, v):  # Input: 360-degree h value, 100% s and v values
    return h/2, s/100*255, v/100*255


class Camera:
    focal_length = 637.647

    def __init__(self, src=0, res=None):
        self.stream = cv.VideoCapture(src)
        if res is not None:
            self.stream.set(cv.CAP_PROP_FRAME_WIDTH, res[0])
            self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, res[1])
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.main_thread = Thread(target=self.update, daemon=True)
        self.main_thread.start()
        #self.sender = imagezmq.ImageSender(connect_to="tcp://ggdev.local:5555")

    def __del__(self):
        if not self.stopped:
            self.stop()
            self.main_thread.join()

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
            #self.sender.send_image("pitesting.local", self.frame)

    def read(self):
        try:
            return self.frame.copy()
        except AttributeError:
            print("Frame not found.")

    def stop(self):
        self.stopped = True

    def getRes(self):
        return self.stream.get(cv.CAP_PROP_FRAME_WIDTH), self.stream.get(cv.CAP_PROP_FRAME_HEIGHT)


line_colors = {'orange': [np.array([7, 100, 93]), np.array([15, 255, 255])],
               'blue': [np.array([100, 180, 50]), np.array([125, 255, 255])]}

block_colors = {'orange': [np.array([7, 100, 93]), np.array([15, 220, 255])],
                'blue': [np.array([100, 150, 50]), np.array([125, 255, 255])]}


def _find_color(frame, points, area_min=2500):  # Extrae un color de la imagen.
    mask = cv.inRange(frame, points[0], points[1])  # create mask with boundaries
    cnts = cv.findContours(mask, cv.RETR_TREE,
                           cv.CHAIN_APPROX_SIMPLE)  # find contours from mask
    cnts = imutils.grab_contours(cnts)

    #objs = []
    for c in cnts:
        area = cv.contourArea(c)  # find how big countour is
        if area > area_min:  # only if countour is big enough, then
            # objs.append(c)
            return c


def block_detector(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # conversion to HSV
    boxes = []
    for name, clr in block_colors.items():  # for each color in colors
        c = _find_color(hsv, clr)
        if c is not None:  # call find_color function above
            boxes.append([cv.boundingRect(c), name])
    return boxes


def _find_lines(frame, points, t1=50, t2=150, ap=5, th=200):  # expects an hsv image
    mask = cv.inRange(frame, points[0], points[1])  # create mask with boundaries
    # line detection
    frame = cv.bitwise_and(frame, frame, mask=mask)
    # Apply edge detection method on the image
    edges = cv.Canny(frame, t1, t2, apertureSize=ap)
    cv.imshow("lines", edges)
    cv.waitKey(1)
    # This returns an array of r and theta values
    lines = cv.HoughLines(edges, 1, 0.017453, th)

    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    if lines is None:
        return []
    out_lines = []
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)

        # Stores the value of sin(theta) in b
        b = np.sin(theta)

        # x0 stores the value rcos(theta)
        x0 = a * r

        # y0 stores the value rsin(theta)
        y0 = b * r

        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000 * (-b))

        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000 * (a))

        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000 * (-b))

        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000 * (a))

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        #cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        out_lines.append([(x1, y1), (x2, y2)])
    return out_lines


def line_detector(frame, **kwargs):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lines = []
    for name, clr in line_colors.items():
        line_set = _find_lines(hsv, clr, **kwargs)
        if line_set:
            lines.append((line_set, name))
    return lines

