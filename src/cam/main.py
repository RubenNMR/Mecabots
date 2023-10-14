import cv2

# item_distance = 32cm
# item length = 271
# px length = 271
# focal length = 637.647


# item width = 6
# item distance = 30
# px width = 152


camara = cv2.VideoCapture(0)
#img = cv2.imread("./testing.png")

def get_focal_length(px_width, obj_dist, obj_width):
    return px_width*obj_dist/obj_width


def get_distance(obj_px_width, obj_real_width, focal_length=637.647):
    return obj_real_width*focal_length/obj_px_width

if __name__ == "__main__":
    while True:
        
        ret, img = camara.read()
        if cv2.waitKey(1) == ord('y'):
            cv2.imwrite(r".\testing.png", img)
            cv2.destroyAllWindows()
            break
        cv2.imshow("asxf", img)
        cv2.waitKey(1)

camara.release()    
