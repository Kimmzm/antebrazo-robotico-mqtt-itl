Integración de Inteligencia Artificial en el Ecosistema IoT (ESP32-CAM ↔ Python IA)


Implementar un sistema de toma de decisiones inteligente integrando un modelo de IA en el servidor Python. El servidor actuará como el cerebro del proyecto: recibirá telemetría y/o imágenes desde la ESP32-CAM vía MQTT, procesará la información mediante librerías especializadas y enviará comandos de respuesta inmediata hacia los actuadores. Todo el desarrollo debe estar alojado en el repositorio del proyecto.


🛠 Requisitos Técnicos y de IA
1. Pipeline de Inteligencia Artificial
Validación Previa: El modelo de IA debe ser probado con datos estáticos (imágenes locales o datasets) antes de la integración con el flujo MQTT.

Procesamiento en Tiempo Real: El flujo debe ser completo y funcional:

Sensor/Cámara (ESP32) → MQTT → Servidor Python (IA) → MQTT → Actuador (ESP32).

Tecnologías: Uso obligatorio de al menos una librería de IA profesional (OpenCV, MediaPipe, TensorFlow Lite, scikit-learn, etc.).

Rol de la Cámara: La ESP32-CAM debe tener un rol funcional y crítico en el pipeline (ej. detección de objetos, clasificación de imágenes, control por gestos, etc.). No se aceptará su uso como simple visualizador.

2. Estándares de Documentación y Repositorio
Repositorio Obligatorio: El código fuente, el modelo (o el script de carga del mismo) y la documentación deben estar en el repositorio compartido.

Encabezado de Código: Todo script (.py, .ino) debe incluir


"""
OBJETIVO: Integración de IA para [Describir función, ej. Clasificación de residuos]
INTEGRANTES: [Nombres Completos y Códigos]
PROYECTO: [Nombre del Proyecto]
"""
Documentación del Modelo: En el código se debe especificar la precisión aproximada y qué tipo de predicción realiza el modelo.

📊 Criterios de Evaluación y Penalizaciones (CRÍTICO)
La evaluación se basa en la funcionalidad del pipeline. Se aplicarán los siguientes descuentos sobre la nota obtenida:

⚠️ Penalización del 40%: Si el reporte no incluye los problemas y conclusiones individuales de cada integrante. (Deberán detallar retos con el entrenamiento, latencia de la imagen o precisión del modelo).

⚠️ Penalización del 20%: Si los archivos de código o el documento no incluyen los nombres, códigos de integrantes o el objetivo del script.

⚠️ Entrega No Válida: Si no se proporciona el enlace al repositorio actualizado con los archivos de IA.

📋 Checklist de Entrega
[ ] Enlace al Repositorio: Carpeta de IA con scripts documentados y el modelo utilizado.

[ ] Prueba Estática: Evidencia de que el modelo funciona antes de recibir datos por MQTT.

[ ] Pipeline Extremo a Extremo: Demostración de que la IA activa un actuador físico basado en lo que "ve" o "lee".

[ ] IA Funcional: La ESP32-CAM aporta datos esenciales para la lógica del proyecto.

[ ] Sustentación Técnica: El equipo explica la arquitectura del modelo, la precisión y el procesamiento de los datos.

[ ] Análisis Individual: Un apartado por cada integrante con: Problemas encontrados, Soluciones aplicadas y Conclusión personal.

📝 Ejemplo de Análisis Individual (Evita el -40%)
Integrante: [Nombre Completo] - [Código]

Problema: "La latencia al enviar imágenes de la ESP32-CAM por MQTT causaba que el modelo de OpenCV procesara cuadros desactualizados..."

Solución: "Se redujo la resolución de la captura y se implementó un sistema de 'skip-frames' en Python para procesar solo el fotograma más reciente..."

Conclusión: "La integración de IA en un servidor externo permite usar modelos más robustos que no cabrían en la memoria de la ESP32, siempre que la red sea estable."
