# TODO: Check if we have to change lanes while we turn and implement that thing.
# TODO: Measure the actual block with on proper distances.
# TODO: Properly implement odometry
# TODO: Implement bot.changeLane function
# TODO: Measure the turning values for the corners
# TODO: Implement proper motion.

from Robot import Robot
from masking import block_detector, line_detector, Camera, block_width, np

bot = Robot()
cam = Camera()
killsig = 0
turn_thres = 30
min_line_len = 500

frame = np.zeros([480, 640, 3])
waypoints = [0, 90, 180, 270]  # these are the edges to turn.
turn_count = 0
current_point = 0
v, omega = 0, 0
target_line = "orange"
state = "straignt"
lane = "left"
angle = 0
corners = 0

try:
    while not killsig:
        # Inputs
        frame = cam.read()
        frame = frame[len(frame) // 2:]
        target_point = waypoints[current_point+1]
        lines = line_detector(frame)
        w = bot.omega

        # logic to decide the next move
        # First, see if we have to turn

        if state == "straight":
            # Check if we must turn
            for line_set in lines:
                if line_set[1] == target_line:
                    for line in line_set[0]:
                        if ((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2) ** 0.5 > min_line_len:
                            state = "turning"
                            v = 1
                            omega = 1 if target_line == "orange" else -1
                            corners += 1
                            break
                    break

            if state == "straight":  # If we didn't turn:
                blocks = block_detector(frame)  # This returns the bounding boxes
                # Go through all detected blocks
                for box, name in blocks:
                    if name == "red":
                        if lane == "right":
                            v, omega = 1, 0
                        else:
                            if box[2] > block_width:
                                bot.changeLane("left")
                                break

                    elif name == "blue":
                        if lane == "left":
                            v, omega = 1, 0
                        else:
                            if box[2] > block_width:
                                bot.changeLane("right")
                                break

        if state == "turning":  # if we found that we have to turn
            target_angle = waypoints[angle % 4]  # get the goal angle
            if target_line == "orange":
                # Decrementing angles
                # this is clockwise
                if w > target_angle:
                    pass
                else:  # We're done turning
                    v, omega = 0, 0  # stop
                    state = "straight"
                    angle -= 1
            elif target_line == "blue":
                # incrementing angles
                # this is ccw
                if w < target_angle:
                    pass
                else:  # We're done turning
                    v, omega = 0, 0
                    state = "straight"
                    angle += 1

        # Outputs
        bot.move(v, omega)
        killsig = 0 if turn_count < 3 else 1



except KeyboardInterrupt:
    cam.stop()
    bot.exit()