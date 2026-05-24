import smbus
import time

class MLX90614:
    # Direcciones I2C para las lecturas de temperatura
    MLX90614_TA = 0x06  # Temperatura ambiente
    MLX90614_TOBJ1 = 0x07  # Temperatura de objeto 1
    MLX90614_TOBJ2 = 0x08  # Temperatura de objeto 2, si el sensor tiene doble entrada

    def _init_(self, address=0x5A, bus=1):
        """Inicializa el sensor MLX90614 en una dirección específica."""
        self.bus = smbus.SMBus(bus)
        self.address = address

    def read_temperature(self, reg):
        """Lee los datos de temperatura en el registro especificado y los convierte a grados Celsius."""
        temp = self.bus.read_word_data(self.address, reg)
        temp = (temp * 0.02) - 273.15  # Conversión a Celsius
        return temp

    def read_ambient_temperature(self):
        """Devuelve la temperatura ambiente en grados Celsius."""
        return self.read_temperature(self.MLX90614_TA)

    def read_object_temperature