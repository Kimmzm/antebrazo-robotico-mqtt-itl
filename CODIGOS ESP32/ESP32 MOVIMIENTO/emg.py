from machine import ADC, Pin
import time
from move import Move

class EMGServoController:
    def __init__(self, servo_pins, emg_pin):
        self.servos = [Move(pin) for pin in servo_pins]
        
        self.emg_pin = ADC(Pin(emg_pin))
        self.emg_pin.atten(ADC.ATTN_11DB)

    def read_emg(self):
        readings = []
        for _ in range(10):
            readings.append(self.emg_pin.read())
            time.sleep(0.01)
        return sum(readings) // len(readings)
    
    def activar_servos(self):
        for servo in self.servos:
            servo.abrir()
    
    def desactivar_servos(self, angle=170):
        for servo in self.servos:
            servo.cerrar(angle)
    
    def controlar_servos_por_emg(self, umbral=500):
        emg_value = self.read_emg()
        print("Valor EMG:", emg_value)
        
        if emg_value > umbral:
            print("Activación: Cerrando servos")
            self.desactivar_servos(170)
        elif emg_value < umbral:
            print("Desactivación: Abriendo servos")
            self.activar_servos()

    def ejecutar(self, umbral=200):
            self.controlar_servos_por_emg(umbral)