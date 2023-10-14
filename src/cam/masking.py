import cv2 as cv
import numpy as np
import imutils


color = (255,255,255)
# I have defined lower and upper boundaries for each color for my camera
# Strongly recommended finding for your own camera.
# RGB: (r, g, b)
# BGR: (b, g, r)
# OpenCV works in BGR

# colors[un color en especifico]
colors = {'blue': [np.array([95, 255, 85]), np.array([120, 255, 255])],

          'red': [np.array([161, 165, 127]), np.array([178, 255, 255])],

          'yellow': [np.array([16, 0, 99]), np.array([39, 255, 255])],

          'green': [np.array([33, 19, 105]), np.array([77, 255, 255])],

          'black': [np.array([0, 0, 0]), np.array([60, 60, 60])]}

def find_color(frame, points, area_min=5000):  # Extrae un color de la imagen.
    mask = cv.inRange(frame, points[0], points[1])  # create mask with boundaries
    cnts = cv.findContours(mask, cv.RETR_TREE,
                           cv.CHAIN_APPROX_SIMPLE) # find contours from mask
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv.contourArea(c) # find how big countour is
        if area > area_min:       # only if countour is big enough, then
            M = cv.moments(c)
            cx = int(M['m10'] / M['m00']) # calculate X position
            cy = int(M['m01'] / M['m00']) # calculate Y position
            return c, cx, cy

def get_distance(obj_px_width, obj_real_width, focal_length=637.647):
    return obj_real_width*focal_length/obj_px_width

cap = cv.VideoCapture(0)
while cap.isOpened(): #main loop
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #convertion to HSV

    for name, clr in colors.items(): # for each color in colors
        vals = find_color(hsv, clr)
        if vals is not None:  # call find_color function above
            c, cx, cy = vals
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 1)

            cv.circle(frame, (cx, cy), 7, color, -1)  # draw circle
            cv.putText(frame, name, (cx,cy), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1) # put text
            # focal length 2 = 760
            #cv.putText(frame, str(get_distance(w, 11.7,)), (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1)

    cv.imshow("Frame: ", frame) # show image
    if cv.waitKey(1) == ord('q'):
        break  

cap.release()   #idk what it is
cv.destroyAllWindows() # close all windows opened by opencv