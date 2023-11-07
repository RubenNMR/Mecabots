
from networktables import NetworkTables as nt
import keyboard

def main():
    """Just print out some event infomation when keys are pressed."""
    nt.initialize("motosierra.local")
    ctrl = nt.getTable("controller")
    running = True
    while running:
        omega,v = 0,0 #initializing values

        if keyboard.is_pressed("left arrow"):
            omega = 1
            print ("Left arrow pressed")
            print (omega)
        if keyboard.is_pressed("right arrow"):
            omega = -1
            print ("Right arrow pressed")
            print (omega)
        if keyboard.is_pressed("up arrow"):
            v = 1
            print ("Up arrow pressed")
            print(v)
        if keyboard.is_pressed("down arrow"):
            v = -1
            print ("Down arrow pressed")
            print(v)
    ctrl.putNumber("v", v)
    ctrl.putNumber("omega", omega)
if __name__ == "__main__":
    main()