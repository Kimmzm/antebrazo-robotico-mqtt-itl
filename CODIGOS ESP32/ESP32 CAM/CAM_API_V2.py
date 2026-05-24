import camera
from time import sleep
import machine
from machine import Pin
import network
import ubinascii  # Para codificar en Base64
import ujson
import urequests



def conexionWIfi(ssid_, wp2_pass):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid_, wp2_pass)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
    
def tomarFoto():
    #Pin del led de flash
    led = machine.Pin(4, machine.Pin.OUT)
    api_url = "http://3.84.5.26:5000/face/123"  # Cambia por tu API REST
    nombre = "Foto.jpg"
    print (nombre)
    
    try:
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        
        #Establece el brillo
        camera.brightness(1)
        
        #Orientacion normal
        camera.flip(0)

        #Orientación normal
        camera.mirror (0)
        
        #Resolución
        camera.framesize(camera.FRAME_QVGA)

        #contraste
        camera.contrast(2)
        
        #saturacion
        camera.saturation (-2)
               
        #calidad
        camera.quality(10)
        
        # special effects
        camera.speffect(camera.EFFECT_NONE)
         
        # white balance
        camera.whitebalance(camera.WB_NONE)
        
        #Enciende flash
        #led.value(1)
        
        #flash
        led.value(1)
        #Captura la imagen
        sleep (0.5)
        img = camera.capture()
        #print (img)
        
        
        led.value(0)
        foto = {
        "imagen": photo_to_base64(img)
        }
        
        send_photo(api_url, foto)
        #desactivar cámara
        camera.deinit ()
        """
        #Guardar la imagen en el sistema de archivos
        imgFile = open(nombre, "wb")
        imgFile.write(img)
        imgFile.close()
        """
        
    except Exception as err:
    
        print ("Error= "+str (err))
        sleep (2)
    
# Convertir foto a Base64
def photo_to_base64(photo_data):
    print("Convirtiendo foto a Base64...")
    try:
        photo_base64 = ubinascii.b2a_base64(photo_data).decode('utf-8')
        #print("Conversión exitosa", photo_base64)
        return photo_base64
    except Exception as e:
        print("Error al convertir la foto:", str(e))
        return None

def send_photo(url, foto):
    
    #response = urequests.get(url,"/",photo_base64)
    json_data = ujson.dumps(foto)
    try:
        print("Enviando foto...")
        # Encabezados de la solicitud
        #headers = {'Content-Type': 'application/Text'}
        # Hacer el POST
        respuesta = urequests.post(url, data = json_data,headers={"Content-Type": "application/json"})
        print("Código de respuesta:", respuesta.status_code)
        print("Respuesta del servidor:", respuesta.text)
    except Exception as e:
        print("Error al enviar JSON:", e)
    
        
if __name__ == '__main__':
    
    ssid_ = "Mega_2.4G_9CA2"
    wp2_pass = "kzqHYadt"
    BUTTON_PIN = 12  # Cambia al pin GPIO donde conectaste el botón
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    """conexionWIfi(ssid_, wp2_pass)
    tomarFoto("""
    conexionWIfi(ssid_, wp2_pass)
    while True:
        if button.value() == 1:
            tomarFoto()
    """
    ssid_ = "RedJonny"
    wp2_pass = "1234567890"
    """
    
    

    