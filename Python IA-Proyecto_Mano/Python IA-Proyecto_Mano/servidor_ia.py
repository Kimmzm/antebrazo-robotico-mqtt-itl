# -*- coding: utf-8 -*-
"""
OBJETIVO: Integración de IA para reconocimiento de gestos y envío de comandos a la mano robótica.
INTEGRANTES:
García Rodríguez Héctor Mauricio (22240332)
Bernal Tolentino Raziel (22240232)
Zamora Martínez Kimberly Paola del Rocío (22240276)
PROYECTO: Mano Robótica para Lenguaje de Señas
"""

import base64
import json
import cv2
import numpy as np
import paho.mqtt.client as mqtt

BROKER_MQTT = "broker.hivemq.com"
PUERTO_MQTT = 1883

TOPICO_CAMARA = "antebrazoitl/camara/video01"
TOPICO_COMANDO = "antebrazoitl/comando/mano/emotes01"

def clasificar_imagen(imagen):
    alto, ancho, _ = imagen.shape
    area_total = alto * ancho

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, umbral = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

    pixeles_blancos = cv2.countNonZero(umbral)
    porcentaje = pixeles_blancos / area_total

    if porcentaje > 0.60:
        return "GESTO_PAZ"
    elif porcentaje > 0.35:
        return "GESTO_LIKE"
    elif porcentaje > 0.15:
        return "GESTO_ROCA"
    else:
        return "GESTO_REPOSO"

def on_connect(client, userdata, flags, rc):
    print("Servidor IA conectado al broker MQTT.")
    print("Código de conexión:", rc)
    client.subscribe(TOPICO_CAMARA)
    print("Suscrito al tópico:", TOPICO_CAMARA)

def on_message(client, userdata, msg):
    try:
        print("\nImagen recibida desde MQTT.")

        datos = json.loads(msg.payload.decode("utf-8"))
        imagen_base64 = datos.get("imagen", "")

        if not imagen_base64:
            print("El mensaje no contiene imagen.")
            return

        imagen_bytes = base64.b64decode(imagen_base64)
        arreglo = np.frombuffer(imagen_bytes, dtype=np.uint8)
        imagen = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)

        if imagen is None:
            print("No se pudo reconstruir la imagen.")
            return

        comando = clasificar_imagen(imagen)

        print("Predicción generada por IA:", comando)
        client.publish(TOPICO_COMANDO, comando, retain=True)
        print("Comando enviado al actuador:", comando)

    except Exception as e:
        print("Error en servidor IA:", e)

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Servidor_IA_Equipo4")
cliente.on_connect = on_connect
cliente.on_message = on_message

print("Iniciando servidor de IA...")
cliente.connect(BROKER_MQTT, PUERTO_MQTT, 60)
cliente.loop_forever()