from machine import Pin, PWM
from move import Move
import time
#import api


class SignLanguage():
    def __init__(self, servo_pins):

        self.servos = [Move(pin) for pin in servo_pins]
        self.abecedary = {
            'A': [(self.servos[0], 'down', 170), (self.servos[1], 'down', 170), (self.servos[2], 'down', 170), (self.servos[3], 'down', 170), (self.servos[4], 'down', 170)], 
            'B': [(self.servos[0], 'up', None), (self.servos[1], 'up', None), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 170)], 
            'C': [(self.servos[0], 'down', 100), (self.servos[1], 'down', 100), (self.servos[2], 'down', 100), (self.servos[3], 'down', 100), (self.servos[4], 'down', 100)], 
            'D': [(self.servos[0], 'down', 170), (self.servos[1], 'down', 170), (self.servos[2], 'down', 170), (self.servos[3], 'up', None), (self.servos[4], 'down', 170)], 
            'E': [(self.servos[0], 'down', 90), (self.servos[1], 'down', 90), (self.servos[2], 'down', 90), (self.servos[3], 'down', 90), (self.servos[4], 'down', 90)], 
            'F': [(self.servos[0], 'up', None), (self.servos[1], 'up', None), (self.servos[2], 'up', None), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'G': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'H': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'I': [(self.servos[0], 'up', None), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'J': [(self.servos[0], 'up', None), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'K': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 90), (self.servos[3], 'up', None), (self.servos[4], 'up', None)], 
            'L': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'up', None)], 
            'M': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'N': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'O': [(self.servos[0], 'down', 100), (self.servos[1], 'down', 100), (self.servos[2], 'down', 100), (self.servos[3], 'down', 100), (self.servos[4], 'down', 100)], 
            'P': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'Q': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'up', None)], 
            'R': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'S': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'T': [(self.servos[0], 'up', None), (self.servos[1], 'up', None), (self.servos[2], 'up', None), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)], 
            'U': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'V': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'W': [(self.servos[0], 'down', 180), (self.servos[1], 'up', None), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'X': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)], 
            'Y': [(self.servos[0], 'up', None), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'up', None)], 
            'Z': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)],
            ' ': [(None, None, None), (None, None, None), (None, None, None), (None, None, None), (None, None, None)],
            '0': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'up', None)],
            '1': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)],
            '2': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)],
            '3': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'up', None)],
            '4': [(self.servos[0], 'up', None), (self.servos[1], 'down', 180), (self.servos[2], 'down', 180), (self.servos[3], 'up', None), (self.servos[4], 'down', 180)],
            '5': [(self.servos[0], 'down', 180), (self.servos[1], 'down', 180), (self.servos[2], 'up', None), (self.servos[3], 'down', 180), (self.servos[4], 'down', 180)],
        }
    
    def read_word(self, word):
        for letter in word:
            print(f"Procesando letra: {letter}")
            for servo, position, angle in self.abecedary.get(letter.upper(), []):  # Usar get para evitar error si la letra no está
                print(f"Moviendo servo: {servo}, posición: {position}, ángulo: {angle}")
                if position == 'down' and angle is not None:
                    servo.cerrar(angle)
                    print(f"Servo cerrado en ángulo {angle}")
                elif position == 'up':
                    servo.abrir()
                    print("Servo abierto")
            print("---------------")
            time.sleep(1.5)

            
    def detener_servos(self):
        """ Detiene todos los servos de la mano. """
        for servo in self.servos:
            servo.detener()
        print("Servos detenidos.")
        

#pins_servos = [4, 19, 12, 13, 14]




#if __name__ == '__main__':
#llamar metodo en main
 #   ssid_ = "RedJonny"
  #  wp2_pass = ""
    
   # api.conexionWIfi(ssid_, wp2_pass)
#    sign_language = SignLanguage(servo_pins = pins_servos)
    
# Llama al método para mover los servos	
#    sign_language.read_word("Hola")
# Detiene los servos después de un tiempo o cuando lo necesites
 #   sign_language.detener_servos()