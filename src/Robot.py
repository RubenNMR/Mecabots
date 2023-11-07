from gpiozero import Device, AngularServo, Motor  # Librerias para controlar dispositivos
from gpiozero.pins.pigpio import PiGPIOFactory  # Recomendado por la libreria para reducir vibraciones del servo
from threading import Thread
from time import sleep, time
import math
Device.pin_factory = PiGPIOFactory()  # no le des mucha mente
# btw esto requiere instalar pigpio por pip y usar el siguiente comando:
"sudo systemctl enable pigpiod"

# Angular: 15s (14.95) for 1 total circle
# Linear: for 59cm, 3.55 seconds
# Diameter of turning circle: 83cm


class Robot:
    def __init__(self, in1=17, in2=22, servo=18):
        self.motor = Motor(in1, in2)
        self.servo = AngularServo(servo, min_pulse_width=0.0005, max_pulse_width=0.0025)  # Ancho de pulsos PWM
        self.servo.angle = 15  # Poniendo el servo en midship (midship=centro)
        self.v, self.omega = 0, 0
        self.stop_flag = 0
        self.x, self.y, self.w = 0, 0, 0
        self.max_linear_speed = 59 / 3.55  # Linear speed in cm per second
        self.max_angular_speed = (2 * math.pi * 41.5) / 15  # Angular speed in radians per second
        Thread(target=self._move, daemon=True).start()

    def _move(self):
        stop = 0
        prev = time()
        while not stop:
            if self.stop_flag:
                if not self.v and not self.omega:
                    self.v, self.omega = 0, 0
                else:
                    stop = 1
            dt = time()-prev
            prev = time()
            # Primero aseguramos que los valores esten entre -1 y 1
            v = min(max(-1, self.v), 1)
            omega = min(max(-1, self.omega), 1)
            self.servo.angle = 30*omega+15  # Mapear valores entre -1 a 1 -> -15 a 45
            self.motor.value = v
            # Esto usa algo llamado setters. Basicamente es una manera especial de llamar una funcion
            # En vez de self.motor.value(v), se asigna como si fuera una variable, y en la libreria eso ajusta el motor
            # Lo mismo con el servo
            # odometry goes here
            self.odom(dt)
            sleep(0.1)

    def move(self, v=0, omega=0):
        self.v, self.omega = v, omega
        sleep(0.1)

    def exit(self):
        # Esto es para luego, por si se necesita.
        self.stop_flag = 1
        self.move()
        self.servo.close()
        self.motor.close()
        pass

    def changeLane(self, side):
        pass

    def odom(self, dt):
        # Calculate linear speed (v) and angular speed (omega) based on servo angle and motor speed
        v = self.v * self.max_linear_speed  # Adjust max_linear_speed as needed
        omega = -self.omega * self.max_angular_speed  # Adjust max_angular_speed as needed, and negate for counterclockwise rotation

        # Calculate change in x, y, and theta
        self.x += v * math.cos(omega) * dt
        self.y += v * math.sin(omega) * dt
        self.w += omega * dt
        print(f"dT: {dt}, X: {self.x:.5f}cm, Y: {self.y:.5f}cm, W: {self.w:.5f} radians")


if __name__ == '__main__':
    from networktables import NetworkTables as nt
    nt.initialize()
    bot = Robot()
    controller = nt.getTable("controller")
    while True:
        omega = controller.getNumber("omega", 0)
        v = controller.getNumber("v", 0)
        bot.move(v, omega)
