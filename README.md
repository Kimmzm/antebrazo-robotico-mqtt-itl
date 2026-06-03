# antebrazo-robotico-mqtt-itl

# Prótesis de Antebrazo Robótico con Comunicación MQTT
### Instituto Tecnológico de León | Sistemas Programables (Unidad 4)

  
**Integrantes:**
* García Rodríguez Héctor Mauricio (22240332)
* Bernal Tolentino Raziel (22240232)
* Zamora Martínez Kimberly Paola del Rocío (22240276)

---

## 📁 Estructura del Repositorio

El proyecto está organizado en las siguientes secciones funcionales:

* **`Documentacion/`**: Contiene el reporte formal de laboratorio en formato PDF con el diseño institucional, objetivos, conclusiones y la matriz jerárquica.
* **`ESP32/`**: Código principal en MicroPython (`main.py`) para el microcontrolador, encargado de la lectura biomédica y el acoplamiento asíncrono mediante una Capa de Abstracción de Hardware (HAL).
* **`Servidor_Python/`**: Script centralizado de monitoreo (`servidor_monitoreo.py`) ejecutado en la estación base para la recepción de telemetría con estampado de tiempo de alta precisión e inyección de comandos gestuales.

---

## 🛠️ Matriz Jerárquica de Tópicos (Estándar Rígido de 4 Niveles)

La arquitectura de red sigue un esquema de 4 niveles independientes (`proyecto / tipo_nodo / nombre_modulo / id_dispositivo`) para asegurar el desacoplamiento total:

| Tópico Estructurado Completo | Descripción del Mensaje |
| :--- | :--- |
| `antebrazoitl/telemetria/oximetro/pulso01` | Ritmo cardíaco (BPM) y saturación de oxígeno (SpO2). |
| `antebrazoitl/telemetria/termometro/corp01` | Datos de temperatura corporal y ambiente (°C). |
| `antebrazoitl/telemetria/emg/musculo01` | Señal de actividad eléctrica muscular del antebrazo. |
| `antebrazoitl/actuador/servomotor/dedos01` | Retroalimentación del estado angular actual de los servos. |
| `antebrazoitl/comando/mano/emotes01` | Instrucción entrante de pose (LIKE, PAZ, CERRAR PUÑO). |
| `antebrazoitl/comando/camara/video01` | Control operacional del flujo de video de la ESP32-CAM. |

---

## 🏢 Resumen de Arquitectura de Software
Para evitar conflictos de temporización entre el escaneo analógico de los sensores físicos y las solicitudes de red asíncronas de MQTT, se implementó una interfaz **HAL (Hardware Abstraction Layer)**. Esta capa encapsula las llamadas al hardware embebido, permitiendo actualizaciones fluidas en tiempo real sin alterar la calibración original de los módulos.
