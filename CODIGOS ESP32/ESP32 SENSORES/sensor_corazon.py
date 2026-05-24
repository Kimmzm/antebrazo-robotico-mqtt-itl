from machine import Pin, I2C, Timer
from utime import sleep, ticks_us, ticks_diff

# Configuración del bus I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)  # Pines de I2C
MAX30102_ADDR = 0x57  # Dirección I2C del MAX30102

# Registros del sensor MAX30102
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1 = 0x0C  # LED rojo
REG_LED2 = 0x0D  # LED infrarrojo
REG_FIFO_DATA = 0x07  # FIFO datos

# Pines para LED indicador
led = Pin(2, Pin.OUT)

class MAX30102:
    def __init__(self, i2c, scl_pin, sda_pin, led_pin):
        self.i2c = i2c
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.led_pin = Pin(led_pin, Pin.OUT)
        self.history_red = [0] * 32
        self.history_ir = [0] * 32
        self.beat = False
        self.beats_history = []
        self.beats = 0
        self.t_start = ticks_us()
        
    def write_register(self, address, value):
        try:
            self.i2c.writeto_mem(MAX30102_ADDR, address, bytearray([value]))
        except OSError as e:
            print(f"Error de comunicación con el sensor: {e}")

    def read_register(self, address, nbytes=1):
        try:
            return self.i2c.readfrom_mem(MAX30102_ADDR, address, nbytes)
        except OSError as e:
            print(f"Error de comunicación con el sensor: {e}")
            return None

    def setup_sensor(self):
        try:
            # Configurar el modo de operación
            self.write_register(0x06, 0x40)  # Restablecer el sensor
            sleep(1)
            self.write_register(REG_MODE_CONFIG, 0x03)  # Modo de LED rojo e IR
            self.write_register(REG_SPO2_CONFIG, 0x27)  # Configuración de SPO2
            self.write_register(REG_LED1, 0x24)  # Configurar LED rojo
            self.write_register(REG_LED2, 0x24)  # Configurar LED IR
            sleep(1)
            print("Sensor configurado.")
        except Exception as e:
            print(f"Error al configurar el sensor: {e}")
    
    def moving_average(self, data, window_size=10):
        return sum(data[-window_size:]) / len(data[-window_size:])
    
    def calculate_bpm(self, value_red):
        minima = min(self.history_red)
        maxima = max(self.history_red)
        threshold_on = minima + (maxima - minima) * 0.75  # Umbral 75%
        threshold_off = minima + (maxima - minima) * 0.5  # Umbral 50%

        if value_red > 1000:  # Confirmar que haya un dedo
            if not self.beat and value_red > threshold_on:
                self.beat = True
                self.led_pin.on()  # LED encendido indica latido
                t_us = ticks_diff(ticks_us(), self.t_start)
                self.t_start = ticks_us()
                bpm = 60 / (t_us / 1e6)  # Calcular BPM

                if bpm < 500:  # Filtrar valores erróneos
                    self.beats_history.append(bpm)
                    if len(self.beats_history) > 20:  # Aumentar el buffer de 10 a 20 mediciones
                        self.beats_history.pop(0)
                    self.beats = self.moving_average(self.beats_history, 20)  # Promediar las últimas 20 mediciones
            elif self.beat and value_red < threshold_off:
                self.beat = False
                self.led_pin.off()
        else:
            self.led_pin.off()  # Apagar LED si no hay dedo
    
    def calculate_spo2(self, value_red, value_ir):
        dc_red = sum(self.history_red) / len(self.history_red)
        ac_red = max(self.history_red) - min(self.history_red)
        
        dc_ir = sum(self.history_ir) / len(self.history_ir)
        ac_ir = max(self.history_ir) - min(self.history_ir)
        
        if dc_red > 0 and dc_ir > 0:
            ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
            spo2 = 110 - 25 * ratio  # Fórmula empírica
            
            # Limitar el valor de SpO₂ entre 90% y 100% para mayor precisión
            if spo2 > 100:
                spo2 = 100
            elif spo2 < 90:
                spo2 = 90
            
            return spo2
        return None
    
    def update_readings(self):
        fifo_data = self.read_register(REG_FIFO_DATA, 6)
        if fifo_data:
            red_reading = (fifo_data[0] << 8) | fifo_data[1]  # Lectura LED rojo
            ir_reading = (fifo_data[2] << 8) | fifo_data[3]  # Lectura LED IR

            # Actualizar historiales
            self.history_red.pop(0)
            self.history_red.append(red_reading)
            self.history_ir.pop(0)
            self.history_ir.append(ir_reading)

            # Calcular BPM y actualizar SpO₂
            self.calculate_bpm(red_reading)
            return red_reading, ir_reading
        return None, None

    def display_results(self):
        spo2 = self.calculate_spo2(self.history_red[-1], self.history_ir[-1])
        print(f"holaBPM: {round(self.beats, 2)} | SpO₂: {round(spo2, 2) if spo2 else '---'}%")
        return [self.beats, (round(spo2, 2) if spo2 else '---')]
