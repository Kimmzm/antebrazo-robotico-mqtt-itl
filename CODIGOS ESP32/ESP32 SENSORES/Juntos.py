# Juntos.py
from machine import Pin, I2C, Timer
from utime import sleep, ticks_us, ticks_diff  # Importar ticks_diff junto con ticks_us
import ujson
import api

class MLX90614:
    def __init__(self, i2c, scl_pin, sda_pin):
        self.i2c = i2c
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.address = 0x5A
        self.REG_TA = 0x06     # Temperatura ambiente
        self.REG_TOBJ1 = 0x07  # Temperatura objeto

    def read_temp(self, register):
        try:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            temp_raw = int.from_bytes(data, 'little')
            return (temp_raw * 0.02) - 273.15  # Convertir de Kelvin a Celsius
        except OSError as e:
            print(f"Error al leer la temperatura: {e}")
            return None

class MAX30102:
    def __init__(self, i2c, scl_pin, sda_pin, led_pin):
        self.i2c = i2c
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.led = Pin(led_pin, Pin.OUT)
        self.address = 0x57
        self.REG_MODE_CONFIG = 0x09
        self.REG_SPO2_CONFIG = 0x0A
        self.REG_LED1 = 0x0C  # LED rojo
        self.REG_LED2 = 0x0D  # LED infrarrojo
        self.REG_FIFO_DATA = 0x07  # FIFO datos
        self.history_red = [0] * 32
        self.history_ir = [0] * 32
        self.beat = False
        self.beats_history = []
        self.beats = 0
        self.t_start = ticks_us()

    def write_register(self, address, value):
        try:
            self.i2c.writeto_mem(self.address, address, bytearray([value]))
        except Exception as e:
            print(f"Error al escribir en el registro {hex(address)}: {e}")

    def read_register(self, address, nbytes=1):
        try:
            result = self.i2c.readfrom_mem(self.address, address, nbytes)
            return result
        except Exception as e:
            print(f"Error al leer del registro {hex(address)}: {e}")
            return None

    def setup_sensor(self):
        self.write_register(0x06, 0x40)  # Reset del sensor
        sleep(1)
        self.write_register(self.REG_MODE_CONFIG, 0x03)  # Modo de LED rojo e IR
        self.write_register(self.REG_SPO2_CONFIG, 0x27)  # Configuración de SPO2
        self.write_register(self.REG_LED1, 0x24)  # LED rojo (configuración de intensidad)
        self.write_register(self.REG_LED2, 0x24)  # LED IR (configuración de intensidad)
        sleep(1)

    def calculate_bpm(self, value_red):
        minima = min(self.history_red)
        maxima = max(self.history_red)
        threshold_on = minima + (maxima - minima) * 0.75
        threshold_off = minima + (maxima - minima) * 0.5

        if value_red > 1000:  # Confirmación de dedo sobre el sensor
            if not self.beat and value_red > threshold_on:
                self.beat = True
                self.led.on()
                t_us = ticks_diff(ticks_us(), self.t_start)  # Utiliza ticks_diff aquí
                self.t_start = ticks_us()
                bpm = 60 / (t_us / 1e6)
                if bpm < 500:
                    self.beats_history.append(bpm)
                    if len(self.beats_history) > 20:
                        self.beats_history.pop(0)
                    self.beats = self.moving_average(self.beats_history, 20)
            elif self.beat and value_red < threshold_off:
                self.beat = False
                self.led.off()
        else:
            self.led.off()  # Apagar el LED si no hay dedo

    def calculate_spo2(self, value_red, value_ir):
        dc_red = sum(self.history_red) / len(self.history_red)
        ac_red = max(self.history_red) - min(self.history_red)
        dc_ir = sum(self.history_ir) / len(self.history_ir)
        ac_ir = max(self.history_ir) - min(self.history_ir)

        if dc_red > 0 and dc_ir > 0:
            ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
            spo2 = 110 - 25 * ratio
            return max(0, min(100, spo2))
        return None

    def update_readings(self):
        fifo_data = self.read_register(self.REG_FIFO_DATA, 6)
        if fifo_data:
            red_reading = (fifo_data[0] << 8) | fifo_data[1]
            ir_reading = (fifo_data[2] << 8) | fifo_data[3]
            self.history_red.pop(0)
            self.history_red.append(red_reading)
            self.history_ir.pop(0)
            self.history_ir.append(ir_reading)
            self.calculate_bpm(red_reading)
            return red_reading, ir_reading
        else:
            return None, None

class SensorManager:
    def __init__(self):
        # Configuración de buses I2C
        self.i2c1 = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
        self.i2c2 = I2C(1, scl=Pin(18), sda=Pin(23), freq=100000)
        
        # Instanciar los sensores
        self.max30102 = MAX30102(self.i2c1, 22, 21, 2)
        self.mlx90614 = MLX90614(self.i2c2, 18, 23)

    def setup(self):
        self.max30102.setup_sensor()

    def display_results(self, t):
        # Obtener lectura de ambos sensores
        red_reading, ir_reading = self.max30102.update_readings()
        spo2 = self.max30102.calculate_spo2(red_reading, ir_reading)
        temp_objeto = self.mlx90614.read_temp(self.mlx90614.REG_TOBJ1)

        # Mostrar los resultados
        data = {
            "idEsp": "123",
            "temp": temp_objeto,
            "ridmo": round(self.max30102.beats, 2),
            "oxig": round(spo2, 2) if spo2 is not None else 0
        }
        print(data)

    def main(self):
        # Configurar el temporizador
        timer = Timer(0)
        timer.init(period=2000, mode=Timer.PERIODIC, callback=self.display_results)

        # Bucle principal
        while True:
            sleep(0.05)
            
            

if __name__ == '__main__':
    SensorManager().main()

