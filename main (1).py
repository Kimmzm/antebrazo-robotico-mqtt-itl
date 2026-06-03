# =============================================================================
# PROYECTO: Control de Mano Robótica por Bluetooth con ESP32 (MicroPython)
# DESCRIPCIÓN: Recibe tramas seriales ("S:P,I,M,A,M\n") a través de UART2
#              (conectado a un módulo Bluetooth HC-05/HC-06) y controla
#              5 servomotores usando PWM con transiciones ultra suaves.
# =============================================================================

import machine
import time
import math

# --- CONFIGURACIÓN DE PINES PARA SERVOS (ESP32) ---
# Puedes cambiar los pines GPIO si lo requieres
PIN_PULGAR = 13
PIN_INDICE = 12
PIN_MEDIO  = 14
PIN_ANULAR = 27
PIN_MENIQUE = 26

# --- CONFIGURACIÓN DE UART (COMUNICACIÓN BLUETOOTH) ---
# Usamos el UART2 del ESP32 (TX=GPIO 17, RX=GPIO 16) para conectar el HC-05/HC-06
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

# --- CLASE PARA CONTROL DE SERVO DE ALTA PRECISIÓN ---
class ServoSmooth:
    def __init__(self, pin, min_us=500, max_us=2500):
        # Configurar PWM a 50Hz (frecuencia estándar para servos analógicos y digitales)
        self.pwm = machine.PWM(machine.Pin(pin), freq=50)
        self.min_us = min_us
        self.max_us = max_us
        self.pos_actual = 0.0
        self.pos_destino = 0.0
        
        # Mover inicialmente a 0 grados
        self.write_angle(0)
        self.pos_actual = 0.0
        
    def write_angle(self, angle):
        # Limitar ángulo por seguridad mecánica
        angle = max(0.0, min(180.0, angle))
        
        # Convertir ángulo (0-180) a ciclo de trabajo de microsegundos (500us - 2500us)
        us = self.min_us + (angle / 180.0) * (self.max_us - self.min_us)
        
        # En MicroPython del ESP32, el ciclo de trabajo de PWM es de 10 bits (0 a 1023)
        # 50Hz equivale a un período de 20ms (20000us)
        # Ciclo de trabajo de 10 bits = (us / 20000) * 1023
        duty = int((us / 20000.0) * 1023)
        self.pwm.duty(duty)

    def set_target(self, angle):
        self.pos_destino = max(0.0, min(180.0, angle))

    def update(self, speed=0.15):
        # Interpolación lineal suave (smooth sweep)
        if abs(self.pos_actual - self.pos_destino) > 0.5:
            self.pos_actual += (self.pos_destino - self.pos_actual) * speed
            self.write_angle(self.pos_actual)
            return True
        else:
            self.pos_actual = self.pos_destino
            return False

# Inicializar los 5 servos en el ESP32
servos = [
    ServoSmooth(PIN_PULGAR),   # Servos[0]
    ServoSmooth(PIN_INDICE),   # Servos[1]
    ServoSmooth(PIN_MEDIO),    # Servos[2]
    ServoSmooth(PIN_ANULAR),   # Servos[3]
    ServoSmooth(PIN_MENIQUE)   # Servos[4]
]

print("--- ESP32 MANO ROBOTICA EN MICROPYTHON INICIALIZADA ---")
print("Escuchando comandos en UART2 (TX=17, RX=16)...")

buffer = ""

while True:
    # 1. Verificar si hay datos seriales entrantes de Bluetooth
    if uart.any():
        try:
            # Leer los bytes entrantes
            data = uart.read().decode('utf-8')
            for char in data:
                if char == '\n':
                    # Fin de trama detectada, procesar comando
                    buffer = buffer.strip()
                    if buffer.startswith("S:"):
                        # Extraer valores numéricos
                        try:
                            valores_str = buffer[2:].split(',')
                            if len(valores_str) == 5:
                                # Convertir y establecer objetivos para cada servo
                                for i in range(5):
                                    angulo = float(valores_str[i])
                                    servos[i].set_target(angulo)
                                print("Comando recibido -> Pulgar: {:.1f}, Índice: {:.1f}, Medio: {:.1f}, Anular: {:.1f}, Meñique: {:.1f}".format(
                                    servos[0].pos_destino, servos[1].pos_destino, servos[2].pos_destino, servos[3].pos_destino, servos[4].pos_destino
                                ))
                        except Exception as e:
                            print("Error al procesar ángulos:", e)
                    buffer = "" # Limpiar buffer
                elif char != '\r':
                    buffer += char
        except Exception as e:
            # Capturar errores de decodificación de bytes corruptos
            print("Error en comunicación serial:", e)
            buffer = ""

    # 2. Actualizar las posiciones físicas de los servos de manera suave
    hubo_cambio = False
    for servo in servos:
        # Actualizar servo. Retorna True si se movió hacia su destino
        if servo.update(speed=0.15):
            hubo_cambio = True

    # 3. Pequeño delay de ciclo para regular la tasa de refresco (50Hz = ~20ms por ciclo)
    time.sleep_ms(20)
