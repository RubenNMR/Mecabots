from gpiozero import Device, AngularServo, Motor  # Librerias para controlar dispositivos
from gpiozero.pins.pigpio import PiGPIOFactory  # Recomendado por la libreria para reducir vibraciones del servo
Device.pin_factory = PiGPIOFactory()  # no le des mucha mente

# Angular: 15s (14.95) for 1 total circle
# Linear: for 59cm, 3.55 seconds
# Diameter of turning circle: 83cm
"""
Pinout:
Servo: GPIO18
Motors:
    In1: 17
    In2: 22

"""
class Robot:
    def _init_(self, in1=17, in2=22, servo=18):
        self.motor = Motor(in1, in2)
        self.servo = AngularServo(servo, min_pulse_width=0.0005, max_pulse_width=0.0025)  # Ancho de pulsos PWM
        self.servo.angle = 15  # Poniendo el servo en midship (midship=centro)

    def move(self, V=0, omega=0):
        # Primero aseguramos que los valores esten entre -1 y 1
        v = min(max(-1, V), 1)
        omega = min(max(-1, omega), 1)
        self.servo.angle = 30*omega+15  # Mapear valores entre -1 a 1 -> -15 a 45
        self.motor.value = v
        # Esto usa algo llamado setters. Basicamente es una manera especial de llamar una funcion
        # En vez de self.motor.value(v), se asigna como si fuera una variable, y en la libreria eso ajusta el motor
        # Lo mismo con el servo

    def exit(self):
        # Esto es para luego, por si se necesita.
        self.move()
        pass


if __name__ == '__main__':
    from time import sleep
    bot = Robot()
    bot.move(1, 0)  # Straight Line
    sleep(1)
    bot.move(-1, 0)  # Return to where it started
    sleep(1)
    bot.move(1, -1)  # Turn left
    sleep(14.95)  #  Measured time for a full circle
    bot.move(1, 1)
    sleep(14.95)
    bot.move()  # braking (Very unintuitive!!!)