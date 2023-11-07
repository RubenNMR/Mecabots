import cv2 as cv
import imutils
import numpy as np
from masking import Camera

line_colors = {'orange': [np.array([7, 100, 93]), np.array([15, 255, 255])],
               'blue2': [np.array([100, 180, 50]), np.array([125, 255, 255])]}

block_colors = {'orange': [np.array([7, 100, 93]), np.array([15, 220, 255])],
                'blue2': [np.array([100, 150, 50]), np.array([125, 255, 255])]}

frame = np.zeros([480, 640, 3])


def mouseRGB(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        cframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        colorsB = cframe[y,x,0]
        colorsG = cframe[y,x,1]
        colorsR = cframe[y,x,2]
        colors = cframe[y,x]
        print("V: ",colorsR)
        print("S: ",colorsG)
        print("H: ",colorsB)
        print("HSV Format: ", colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)

cv.namedWindow("og")
cv.setMouseCallback("og", mouseRGB)


# TODO: add the distance measurement to return the closest block.
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



if __name__ == '__main__':
    cam = Camera()
    print(cam.getRes())
    lower1, upper1 = block_colors['orange']
    lower2, upper2 = block_colors['blue2']
    while True:
        # cam stuff
        frame = cam.read()
        frame = frame[len(frame)//2:]
        boxes = block_detector(frame)
        lines = line_detector(frame, t1=300, t2=900, ap=3, th=100)

        # masked frame
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower1, upper1)
        mask2 = cv.inRange(hsv, lower2, upper2)
        outFrame = cv.bitwise_or(cv.bitwise_and(frame, frame, mask=mask), cv.bitwise_and(frame, frame, mask=mask2))

        for box in boxes:
            x, y, w, h = box[0]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3, cv.LINE_AA)

        for line_set in lines:
            for line in line_set[0]:
                cv.line(frame, line[0], line[1], (0, 0, 255), 2)

        cv.imshow("og", frame)
        cv.imshow("masks", outFrame)
        cv.waitKey(1)

