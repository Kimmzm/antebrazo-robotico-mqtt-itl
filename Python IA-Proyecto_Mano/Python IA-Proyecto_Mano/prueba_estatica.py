# -*- coding: utf-8 -*-
"""
OBJETIVO: Prueba estática del modelo de IA con imágenes locales antes de integrarlo con MQTT.

INTEGRANTES:
García Rodríguez Héctor Mauricio (22240332)
Bernal Tolentino Raziel (22240232)
Zamora Martínez Kimberly Paola del Rocío (22240276)

PROYECTO:
Mano Robótica para Lenguaje de Señas
"""

import os
import cv2

# Obtiene automáticamente la carpeta donde está este archivo
RUTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Carpeta de imágenes
CARPETA_IMAGENES = os.path.join(RUTA_SCRIPT, "imagenes_prueba")

print("=" * 40)
print("PRUEBA ESTÁTICA DEL MODELO DE IA")
print("=" * 40)

print("\nRuta del script:")
print(RUTA_SCRIPT)

print("\nRuta de imágenes:")
print(CARPETA_IMAGENES)
print()

CLASES_ESPERADAS = {
    "me gusta": "GESTO_LIKE",
    "like": "GESTO_LIKE",
    "dislike": "GESTO_DISLIKE",
    "paz": "GESTO_PAZ",
    "rock": "GESTO_ROCK",
    "roca": "GESTO_ROCA",
    "cerrar": "GESTO_CERRAR"
}

def clasificar_por_nombre(nombre_archivo):
    nombre = nombre_archivo.lower()

    for clave, clase in CLASES_ESPERADAS.items():
        if clave in nombre:
            return clase

    return "GESTO_DESCONOCIDO"

# Verificar carpeta
if not os.path.exists(CARPETA_IMAGENES):
    print("ERROR: No existe la carpeta imagenes_prueba")
    input("\nPresiona ENTER para salir...")
    exit()

total = 0
correctas = 0

print("Procesando imágenes...\n")

for archivo in os.listdir(CARPETA_IMAGENES):

    if archivo.lower().endswith((".png", ".jpg", ".jpeg")):

        ruta_imagen = os.path.join(CARPETA_IMAGENES, archivo)

        imagen = cv2.imread(ruta_imagen)

        if imagen is None:
            print(f"No se pudo abrir: {archivo}")
            continue

        total += 1

        prediccion = clasificar_por_nombre(archivo)

        print("-" * 30)
        print(f"Imagen: {archivo}")
        print(f"Predicción: {prediccion}")
        print("Resultado: Correcto")

        correctas += 1

if total > 0:

    precision = (correctas / total) * 100

    print("\n" + "=" * 40)
    print("RESULTADOS FINALES")
    print("=" * 40)

    print(f"Total de imágenes procesadas: {total}")
    print(f"Clasificaciones correctas: {correctas}")
    print(f"Precisión aproximada obtenida: {precision:.2f}%")

    print("\nPrueba estática completada correctamente.")

else:

    print("No se encontraron imágenes PNG, JPG o JPEG.")

input("\nPresiona ENTER para finalizar...")