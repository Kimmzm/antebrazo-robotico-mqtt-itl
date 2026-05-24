import network
import urequests
import ujson

# ---------------------CONEXION WIFI-----------------
def conexionWIfi(ssid_, wp2_pass):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid_, wp2_pass)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
    
# -----------------------conexión api-----------------------
def send_word(url, datos):
    #print("Enviando foto...")
#response = urequests.get(url,"/",photo_base64)
    try:
        # Encabezados de la solicitud
        headers = {'Content-Type': 'application/json'}
        #Hacer el POST
        respuesta = urequests.post(url, headers=headers, data = datos)
        #print("Código de respuesta:", respuesta.status_code)
        #print("Respuesta del servidor:", respuesta.text)
        palabra = ujson.loads(respuesta.text)  
        
    except Exception as e:
        print("Error al enviar JSON:", e)
        return None
    
    return  palabra.get('Respuesta', None)

def enter(url):
    
    try:
        respuesta = urequests.get(url)
        print("Código de respuesta:", respuesta.status_code)
        print("Respuesta del servidor:", respuesta.text)
        reconocimiento = ujson.loads(respuesta.text)
        
    except Exception as e:
        print("Error al enviar JSON:", e)
        return None
    
    return  reconocimiento.get('Respuesta', None)



