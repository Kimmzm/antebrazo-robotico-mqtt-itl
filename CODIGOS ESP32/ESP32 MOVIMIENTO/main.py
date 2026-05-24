from machine import Pin
from machine import Timer
from array import array
from utime import ticks_us
from utime import ticks_diff

class IR_RX():
    # Result/error codes
    # Repeat button code
    REPEAT = -1
    # Error codes
    BADSTART = -2
    BADBLOCK = -3
    BADREP = -4
    OVERRUN = -5
    BADDATA = -6
    BADADDR = -7

    def __init__(self, pin, nedges, tblock, callback, *args):  # Optional args for callback
        self._pin = pin
        self._nedges = nedges
        self._tblock = tblock
        self.callback = callback
        self.args = args
        self._errf = lambda _ : None
        self.verbose = False

        self._times = array('i',  (0 for _ in range(nedges + 1)))  # +1 for overrun
        pin.irq(handler = self._cb_pin, trigger = (Pin.IRQ_FALLING | Pin.IRQ_RISING))
        self.edge = 0
        self.tim = Timer(-1)  # Sofware timer
        self.cb = self.decode

    # Pin interrupt. Save time of each edge for later decode.
    def _cb_pin(self, line):
        t = ticks_us()
        # On overrun ignore pulses until software timer times out
        if self.edge <= self._nedges:  # Allow 1 extra pulse to record overrun
            if not self.edge:  # First edge received
                self.tim.init(period=self._tblock , mode=Timer.ONE_SHOT, callback=self.cb)
            self._times[self.edge] = t
            self.edge += 1

    def do_callback(self, cmd, addr, ext, thresh=0):
        self.edge = 0
        if cmd >= thresh:
            self.callback(cmd, addr, ext, *self.args)
        else:
            self._errf(cmd)

    def error_function(self, func):
        self._errf = func

    def close(self):
        self._pin.irq(handler = None)
        self.tim.deinit()


class NEC_ABC(IR_RX):
    def __init__(self, pin, extended, callback, *args):
        # Block lasts <= 80ms (extended mode) and has 68 edges
        super().__init__(pin, 68, 80, callback, *args)
        self._extended = extended
        self._addr = 0

    def decode(self, _):
        try:
            if self.edge > 68:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < 4000:  # 9ms leading mark for all valid data
                raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > 3000:  # 4.5ms space for normal data
                if self.edge < 68:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                val = 0
                for edge in range(3, 68 - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:
                        val |= 0x80000000
            elif width > 1700: # 2.5ms space for a repeat code. Should have exactly 4 edges.
                raise RuntimeError(self.REPEAT if self.edge == 4 else self.BADREP)  # Treat REPEAT as error.
            else:
                raise RuntimeError(self.BADSTART)
            addr = val & 0xff  # 8 bit addr
            cmd = (val >> 16) & 0xff
            if cmd != (val >> 24) ^ 0xff:
                raise RuntimeError(self.BADDATA)
            if addr != ((val >> 8) ^ 0xff) & 0xff:  # 8 bit addr doesn't match check
                if not self._extended:
                    raise RuntimeError(self.BADADDR)
                addr |= val & 0xff00  # pass assumed 16 bit address to callback
            self._addr = addr
        except RuntimeError as e:
            cmd = e.args[0]
            addr = self._addr if cmd == self.REPEAT else 0  # REPEAT uses last address
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0, self.REPEAT)

class NEC_8(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, False, callback, *args)

class NEC_16(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, callback, *args)

#-------------------------------------------------------
#CÓDIGO PARA EL FUNCIONAMIENTO CORRECTO DEL INFRARROJO
import time
from machine import Pin, freq, PWM

pin_ir = Pin(23, Pin.IN)

def decodeKeyValue(data):
    if data == 0x68:
        return "0" 
    if data == 0x30:
        return "1"
    if data == 0x18:
        return "2" 
    if data == 0x7A:
        return "3"
    if data == 0x10:
        return "4"
    if data == 0x38:
        return "5"
    if data == 0x5A:
        return "6"
    if data == 0x42:
        return "7"
    if data == 0x4A:
        return "8"
    if data == 0x52:
        return "9"
    if data == 0x2:
        return "+"
    if data == 0x98:
        return "-"
    if data == 0x90:
        return "FORWARD"
    if data == 0xE0:
        return "BACKWARD"
    if data == 0xA8:
        return "PLAY/PAUSE"
    if data == 0xC2:
        return "BACK"
    if data == 0xA2:
        return "POWER/OFF"
    if data == 0x22:
        return "TEST"
    if data == 0xE2:
        return "MENU" 
    if data == 0xB0:
        return "C" 
    return hex(data)
#--------------------------------------
in1 = Pin(2, Pin.OUT)
in2 = Pin(4, Pin.OUT)
ena = PWM(Pin(15), freq=1000)

in3 = Pin(18, Pin.OUT)
in4 = Pin(19, Pin.OUT)
enb = PWM(Pin(5), freq=1000)

def motor1_forward(speed):
    in1.value(1)
    in2.value(0)
    ena.duty(int(speed * 1023 / 100))

def motor1_backward(speed):
    in1.value(0)
    in2.value(1)
    ena.duty(int(speed * 1023 / 100))

def motor1_stop():
    in1.value(0)
    in2.value(0)
    ena.duty(0)

def motor2_forward(speed):
    in3.value(1)
    in4.value(0)
    enb.duty(int(speed * 1023 / 100))  # Ajuste de velocidad (0-100%)

def motor2_backward(speed):
    in3.value(0)
    in4.value(1)
    enb.duty(int(speed * 1023 / 100))

def motor2_stop():
    in3.value(0)
    in4.value(0)
    enb.duty(0)
        
#-------------------------------------

def callback(data, addr, ctrl):
    if data < 0:
        pass
    else:
        if str(data) == "24":
            motor1_forward(100)
            motor2_forward(100)
        elif str(data) == "82":
            motor1_backward(100)
            motor2_backward(100)
        elif str(data) == "8":
            motor1_forward(100)
            motor2_stop()
        elif str(data) == "90":
            motor2_forward(100)
            motor1_stop()
        else:
            motor1_stop()
            motor2_stop()
        print(str(data))
        #print(decodeKeyValue(data))


ir = NEC_8(pin_ir, callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    ir.close()
    