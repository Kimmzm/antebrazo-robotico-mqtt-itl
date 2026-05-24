"""
OBJETIVO: Servidor de monitoreo biomédico y control de emotes para la prótesis de antebrazo.
INTEGRANTES: 
    García Rodríguez Héctor Mauricio (22240332)
    Bernal Tolentino Raziel (22240232)
    Zamora Martínez Kimberly Paola del Rocío (22240276)
PROYECTO: Antebrazo Robótico MQTT - ITL
"""
import paho.mqtt.client as mqtt
import datetime
import time

BROKER_MQTT = "broker.hivemq.com"
PORT_MQTT = 1883
TOPICO_TELEMETRIA = "antebrazoitl/telemetria/#"
TOPICO_COMANDOS = "antebrazoitl/comando/mano/emotes01"

def on_connect(client, userdata, flags, rc):
    print(f"Conexión exitosa al broker con código de resultado: {rc}")
    client.subscribe(TOPICO_TELEMETRIA)

def on_message(client, userdata, msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    payload_decodificado = msg.payload.decode()
    print(f"[{timestamp}] [TELEMETRÍA] Tópico: {msg.topic} | Valor Recibido: {payload_decodificado}")

server_client = mqtt.Client("ITL_Server_Python_Mano")
server_client.on_connect = on_connect
server_client.on_message = on_message

print("Iniciando Servidor de Monitoreo de Antebrazo Robótico...")
server_client.connect(BROKER_MQTT, PORT_MQTT, 60)
server_client.loop_start()

try:
    while True:
        print("\n--- PANEL DE CONTROL DE EMOTES (COMANDOS DE SEÑAS) ---")
        print("1. Gesto: LIKE (Pulgar arriba)")
        print("2. Gesto: PAZ Y AMOR")
        print("3. Gesto: CERRAR PUÑO")
        print("4. Gesto: ABRIR MANO (Posición de Reposo)")
        opcion = input("Selecciona el comando a enviar al antebrazo: ")
        
        if opcion == "1":
            server_client.publish(TOPICO_COMANDOS, "GESTO_LIKE")
        elif opcion == "2":
            server_client.publish(TOPICO_COMANDOS, "GESTO_PAZ")
        elif opcion == "3":
            server_client.publish(TOPICO_COMANDOS, "GESTO_CERRAR")
        elif opcion == "4":
            server_client.publish(TOPICO_COMANDOS, "GESTO_REPOSO")
        time.sleep(2)
except KeyboardInterrupt:
    server_client.loop_stop()
    server_client.disconnect()
