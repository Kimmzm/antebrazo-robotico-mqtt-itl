# -*- coding: utf-8 -*-
"""
OBJETIVO: Enviar una imagen local por MQTT para validar el pipeline IA antes de usar la ESP32-CAM física.
INTEGRANTES:
García Rodríguez Héctor Mauricio (22240332)
Bernal Tolentino Raziel (22240232)
Zamora Martínez Kimberly Paola del Rocío (22240276)
PROYECTO: Mano Robótica para Lenguaje de Señas
"""

import base64
import json
import paho.mqtt.client as mqtt

BROKER_MQTT = "broker.hivemq.com"
PUERTO_MQTT = 1883
TOPICO_CAMARA = "antebrazoitl/camara/video01"

RUTA_IMAGEN = "imagenes_prueba/me gusta.png"

with open(RUTA_IMAGEN, "rb") as archivo:
    imagen_base64 = base64.b64encode(archivo.read()).decode("utf-8")

mensaje = {
    "dispositivo": "ESP32-CAM-SIMULADA",
    "imagen": imagen_base64
}

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "ESP32_CAM_Simulada_Equipo4")
cliente.connect(BROKER_MQTT, PUERTO_MQTT, 60)

cliente.publish(TOPICO_CAMARA, json.dumps(mensaje), retain=True)

print("Imagen enviada correctamente por MQTT.")
print("Tópico:", TOPICO_CAMARA)

cliente.disconnect()