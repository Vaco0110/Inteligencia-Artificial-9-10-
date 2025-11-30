# README.md - Detector de Emociones Faciales con FER-2013
# Descripción del Proyecto
Sistema completo de reconocimiento de emociones faciales en tiempo real utilizando Deep Learning y el dataset FER-2013. Detecta 4 emociones principales: >:( Enojo, :) Felicidad, ._. Neutral, <:,( Tristeza.

# Requisitos

Librerías Principales (CRÍTICAS)
Librería              	Versión	            Propósito
tensorflow	            2.13.0	            Framework de ML/DL principal
opencv-python-headless	4.8.1.78	          Procesamiento de imágenes y video
matplotlib	            3.7.1	              Visualización y gráficas
numpy	                  1.24.3	            Operaciones numéricas
pillow	                9.5.0	              Procesamiento de imágenes

Librerías de Machine Learning
Librería	              Versión	            Propósito
keras                  	2.13.1	            API de alto nivel para TensorFlow
scikit-learn	          1.3.0	              Métricas y evaluación
scikit-image	          0.21.0	            Procesamiento avanzado de imágenes
imutils	                0.5.4	              Utilidades para visión por computadora

Librerías de Datos y Utilidades
Librería	              Versión             Propósito
pandas	                2.0.3	              Manipulación de datos
seaborn	                0.12.2	            Visualización estadística
plotly	                5.15.0	            Gráficas interactivas
tqdm	                  4.65.0	            Barras de progreso
psutil	                5.9.5	              Monitoreo de sistema

Librerías para Dataset
Librería	              Versión	            Propósito
kaggle	                1.5.16	            Descarga de dataset FER-2013
wget	                  3.2	                Descargas alternativas

# Características:

- Detección en tiempo real con cámara web

- Interfaz visual con barras de probabilidad

- Sistema de estabilización para predicciones suaves

- Controles: 'Q' para salir, 'R' para resetear


# Resultados Esperados
- Métricas de Rendimiento
Precisión en validación: 50-70%

FPS en tiempo real: 15-30 FPS

Latencia de predicción: 50-100ms

- Características del Modelo
Arquitectura: MobileNetV2 + Capas Personalizadas

Input: 48x48 píxels RGB

Output: 4 emociones con probabilidades

Optimización: Fine-tuning con aumento de datos
