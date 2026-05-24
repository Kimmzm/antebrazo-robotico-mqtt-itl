# sensor_temperatura.py
from machine import I2C, Pin

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
