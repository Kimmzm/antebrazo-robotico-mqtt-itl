from machine import Pin, I2C, Timer
from utime import sleep, ticks_us, ticks_diff
import api
import ujson

# Configuración del bus I2C para ambos sensores
i2c1 = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)  # MAX30102

i2c2 = I2C(1, scl=Pin(18), sda=Pin(23), freq=100000)  # MLX90614

# Configuración del MAX30102
MAX30102_ADDR = 0x57
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1 = 0x0C  # LED rojo
REG_LED2 = 0x0D  # LED infrarrojo
REG_FIFO_DATA = 0x07  # FIFO datos
led = Pin(2, Pin.OUT)  # LED indicador del MAX30102

# Configuración del MLX90614
MLX90614_I2CADDR = 0x5A
MLX90614_TA = 0x06     # Temperatura ambiente
MLX90614_TOBJ1 = 0x07  # Temperatura objeto

# Funciones para el MAX30102
def write_register(address, value):
    i2c1.writeto_mem(MAX30102_ADDR, address, bytearray([value]))

def read_register(address, nbytes=1):
    return i2c1.readfrom_mem(MAX30102_ADDR, address, nbytes)

def setup_sensor():
    write_register(0x06, 0x40)  # Reset del sensor
    sleep(1)
    write_register(REG_MODE_CONFIG, 0x03)  # Modo de LED rojo e IR
    write_register(REG_SPO2_CONFIG, 0x27)  # Configuración de SPO2
    write_register(REG_LED1, 0x24)  # LED rojo
    write_register(REG_LED2, 0x24)  # LED IR
    sleep(1)
    print("MAX30102 configurado.")

history_red = [0] * 32
history_ir = [0] * 32
beat = False
beats_history = []
beats = 0
t_start = ticks_us()

def calculate_bpm(value_red):
    global beat, beats, t_start, beats_history

    minima = min(history_red)
    maxima = max(history_red)
    threshold_on = minima + (maxima - minima) * 0.75
    threshold_off = minima + (maxima - minima) * 0.5

    if value_red > 1000:
        if not beat and value_red > threshold_on:
            beat = True
            led.on()
            t_us = ticks_diff(ticks_us(), t_start)
            t_start = ticks_us()
            bpm = 60 / (t_us / 1e6)

            if bpm < 500:
                beats_history.append(bpm)
                if len(beats_history) > 10:
                    beats_history.pop(0)
                beats = sum(beats_history) / len(beats_history)
        elif beat and value_red < threshold_off:
            beat = False
            led.off()
    else:
        led.off()

def calculate_spo2(value_red, value_ir):
    dc_red = sum(history_red) / len(history_red)
    ac_red = max(history_red) - min(history_red)
    dc_ir = sum(history_ir) / len(history_ir)
    ac_ir = max(history_ir) - min(history_ir)
    if dc_red > 0 and dc_ir > 0:
        ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
        spo2 = 110 - 25 * ratio
        spo2 = max(0, min(100, spo2))
        return spo2
    return None

# Funciones para el MLX90614
def read_temp(register):
    try:
        data = i2c2.readfrom_mem(MLX90614_I2CADDR, register, 2)
        temp_raw = int.from_bytes(data, 'little')
        return (temp_raw * 0.02) - 273.15
    except OSError as e:
        print(f"Error al leer el registro {register}: {e}")
        return None

# Mostrar resultados de ambos sensores
def display_results(t):
    global beats
    spo2 = calculate_spo2(history_red[-1], history_ir[-1])
    temp_ambiente = read_temp(MLX90614_TA)
    temp_objeto = read_temp(MLX90614_TOBJ1)
    
    
    data = {
            "idEsp": "123",
            "temp": temp_objeto,
            "ridmo": round(beats, 2),
            "oxig": round(spo2, 2) if spo2 else '---'
        }
    print(data)
    
    api.send_word("http://192.168.70.11:5000/setSensor", ujson.dumps(data))
    

ssid_ = "RedJonny"
wp2_pass = "1234567890"
    
api.conexionWIfi(ssid_, wp2_pass)


# Configurar el temporizador
timer = Timer(0)
timer.init(period=2000, mode=Timer.PERIODIC, callback=display_results)

# Inicializar sensores
setup_sensor()

# Bucle principal
while True:
    # Leer datos del MAX30102
    fifo_data = read_register(REG_FIFO_DATA, 6)
    red_reading = (fifo_data[0] << 8) | fifo_data[1]
    ir_reading = (fifo_data[2] << 8) | fifo_data[3]

    history_red.pop(0)
    history_red.append(red_reading)
    history_ir.pop(0)
    history_ir.append(ir_reading)

    calculate_bpm(red_reading)
    sleep(0.05)
