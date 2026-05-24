from machine import Pin, PWM
import time

class Move():
    def __init__(self, p):
        self.pin = Pin(p, Pin.OUT)
        self.servo = PWM(self.pin)
        self.servo.freq(50)
    
    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max-in_min) + out_min)

    def move(self, angle):
        # Mapea el ángulo (0-180) a un valor de PWM (20-120)
        duty = self.map(angle, 0, 180, 30, 115)  # Ajuste los valores aquí si es necesario
        self.servo.duty(duty)

    def abrir(self):
        self.move(0)
        return None

    def cerrar(self, angle):
        self.move(angle)
        return None
    
    def detener(self):
        """ Detiene el servo, apagando el PWM. """
        self.servo.deinit()
