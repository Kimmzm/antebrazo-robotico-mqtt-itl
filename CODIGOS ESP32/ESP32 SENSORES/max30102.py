from machine import Pin, I2C, Timer
from utime import sleep, ticks_us, ticks_diff


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
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def read_register(self, address, nbytes=1):
        return self.i2c.readfrom_mem(self.address, address, nbytes)

    def setup_sensor(self):
        self.write_register(0x06, 0x40)  # Reset del sensor
        sleep(1)
        self.write_register(self.REG_MODE_CONFIG, 0x03)  # Modo de LED rojo e IR
        self.write_register(self.REG_SPO2_CONFIG, 0x27)  # Configuración de SPO2
        self.write_register(self.REG_LED1, 0x24)  # LED rojo
        self.write_register(self.REG_LED2, 0x24)  # LED IR
        sleep(1)
       # print("MAX30102 configurado.")

    def calculate_bpm(self, value_red):
        minima = min(self.history_red)
        maxima = max(self.history_red)
        threshold_on = minima + (maxima - minima) * 0.75
        threshold_off = minima + (maxima - minima) * 0.5

        if value_red > 1000:
            if not self.beat and value_red > threshold_on:
                self.beat = True
                self.led.on()
                t_us = ticks_diff(ticks_us(), self.t_start)
                self.t_start = ticks_us()
                bpm = 60 / (t_us / 1e6)

                if bpm < 500:
                    self.beats_history.append(bpm)
                    if len(self.beats_history) > 10:
                        self.beats_history.pop(0)
                    self.beats = sum(self.beats_history) / len(self.beats_history)
            elif self.beat and value_red < threshold_off:
                self.beat = False
                self.led.off()
        else:
            self.led.off()


    def calculate_spo2(self, value_red, value_ir):
        dc_red = sum(self.history_red) / len(self.history_red)
        ac_red = max(self.history_red) - min(self.history_red)
        dc_ir = sum(self.history_ir) / len(self.history_ir)
        ac_ir = max(self.history_ir) - min(self.history_ir)

        #print(f"dc_red: {dc_red}, ac_red: {ac_red}, dc_ir: {dc_ir}, ac_ir: {ac_ir}")  # Debugging line

        if dc_red > 0 and dc_ir > 0:
            ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
            spo2 = 110 - 25 * ratio
            return max(0, min(100, spo2))
        return None


    def update_readings(self):
        fifo_data = self.read_register(self.REG_FIFO_DATA, 6)
        red_reading = (fifo_data[0] << 8) | fifo_data[1]
        ir_reading = (fifo_data[2] << 8) | fifo_data[3]

        #print(f"red_reading: {red_reading}, ir_reading: {ir_reading}")  # Debugging line

        self.history_red.pop(0)
        self.history_red.append(red_reading)
        self.history_ir.pop(0)
        self.history_ir.append(ir_reading)

        self.calculate_bpm(red_reading)
        return red_reading, ir_reading
