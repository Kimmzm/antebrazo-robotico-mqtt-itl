from machine import Pin, I2C, Timer
from utime import sleep, ticks_us, ticks_diff


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
            return (temp_raw * 0.02) - 273.15
        except OSError as e:
            #print(f"Error al leer el registro {register}: {e}")
            return None