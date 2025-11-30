"""
DETECTOR DE EMOCIONES FACIALES - 4 CLASES
--------------------------------------------------------------------
Detecta: happy, sad, angry, neutral
Optimizado para FER-2013 con estabilización mejorada
"""

"""
!!! Favor de cambiar el campo RUTA_CARPETA con la ubiacion de su modelo entrenado con terminación .h5 para su ejecución correcta !!!
"""
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import sys
from collections import deque

# ============================================================================
# CONFIGURACIÓN GPU en caso de tener una 
# ============================================================================
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("✅ GPU detectada y configurada")
    except RuntimeError as e:
        print(f"⚠️ Error GPU: {e}")

# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class DetectorEmociones4Clases:
    def __init__(self, ruta_modelo):
        print("\n" + "="*70)
        print("🎥 DETECTOR DE EMOCIONES FACIALES (4 CLASES)")
        print("="*70)

        # 1. CARGAR MODELO
        try:
            print(f"📦 Cargando modelo: {ruta_modelo}...")
            self.modelo = keras.models.load_model(ruta_modelo)
            print("✅ Modelo cargado exitosamente")
        except Exception as e:
            print(f"❌ ERROR FATAL: {e}")
            sys.exit(1)

        # 2. CONFIGURACIÓN DE EMOCIONES (4 CLASES)
        # El orden debe coincidir con el del entrenamiento
        self.emociones = ['angry', 'happy', 'neutral', 'sad']
        
        # Verificar salidas del modelo
        num_salidas = self.modelo.output_shape[-1]
        if num_salidas != 4:
            print(f"⚠️ ADVERTENCIA: El modelo tiene {num_salidas} salidas")
            print(f"   Se esperaban 4. Verificando orden de clases...")
        
        self.img_size = self.modelo.input_shape[1]
        print(f"📐 Tamaño de entrada: {self.img_size}x{self.img_size}")

        # 3. DETECTOR DE ROSTROS
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            print("❌ ERROR: No se pudo cargar el detector de rostros")
            sys.exit(1)

        # 4. SISTEMA DE ESTABILIZACIÓN AVANZADO
        self.historial_predicciones = deque(maxlen=15)  # Memoria extendida
        self.ultima_emocion = None
        self.contador_estabilidad = 0
        self.umbral_confianza = 0.45  # Umbral mínimo de confianza

        # 5. COLORES VIBRANTES POR EMOCIÓN
        self.colores = {
            'angry': (0, 0, 255),      # Rojo
            'happy': (0, 255, 255),    # Amarillo
            'neutral': (180, 180, 180),# Gris
            'sad': (255, 100, 0)       # Azul
        }

        # 6. EMOJIS
        self.emojis = {
            'angry': '😠',
            'happy': '😊',
            'neutral': '😐',
            'sad': '😢'
        }

        print(f"🎯 Emociones detectables: {self.emociones}")
        print("="*70 + "\n")

    def preprocesar_rostro(self, rostro):
        """
        Preprocesa el rostro para el modelo
        Convierte a RGB y normaliza
        """
        try:
            # Redimensionar
            img = cv2.resize(rostro, (self.img_size, self.img_size))
            
            # Convertir a RGB (el modelo espera RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Normalizar
            img = img.astype(np.float32) / 255.0
            
            # Expandir dimensiones para batch
            return np.expand_dims(img, axis=0)
            
        except Exception as e:
            print(f"⚠️ Error en preprocesamiento: {e}")
            return None

    def predecir_emocion(self, rostro):
        """
        Predice la emoción con sistema de estabilización
        """
        roi_procesada = self.preprocesar_rostro(rostro)
        
        if roi_procesada is None:
            return None, None, None
        
        # Predicción del modelo
        prediccion_raw = self.modelo.predict(roi_procesada, verbose=0)[0]
        
        # Agregar al historial
        self.historial_predicciones.append(prediccion_raw)
        
        # Suavizar con promedio de historial
        if len(self.historial_predicciones) >= 5:
            prediccion_suavizada = np.mean(list(self.historial_predicciones)[-10:], axis=0)
        else:
            prediccion_suavizada = prediccion_raw
        
        # Obtener emoción con mayor probabilidad
        idx = np.argmax(prediccion_suavizada)
        emocion = self.emociones[idx]
        confianza = prediccion_suavizada[idx]
        
        # Sistema anti-parpadeo
        if confianza < self.umbral_confianza:
            if self.ultima_emocion is not None:
                emocion = self.ultima_emocion
        else:
            if self.ultima_emocion == emocion:
                self.contador_estabilidad += 1
            else:
                self.contador_estabilidad = 0
            self.ultima_emocion = emocion
        
        return emocion, confianza, prediccion_suavizada

    def dibujar_interfaz(self, frame, rostros_info):
        """
        Dibuja la interfaz completa con rostros y estadísticas
        """
        canvas = frame.copy()
        
        for info in rostros_info:
            x, y, w, h = info['bbox']
            emocion = info['emocion']
            confianza = info['confianza']
            prediccion = info['prediccion']
            
            color = self.colores.get(emocion, (255, 255, 255))
            
            # Rectángulo del rostro
            cv2.rectangle(canvas, (x, y), (x+w, y+h), color, 3)
            
            # Etiqueta con emoji
            emoji = self.emojis.get(emocion, '')
            label = f"{emoji} {emocion.upper()}"
            confianza_text = f"{confianza*100:.0f}%"
            
            # Fondo de etiqueta
            label_height = 50
            cv2.rectangle(canvas, (x, y-label_height), (x+w, y), color, -1)
            
            # Texto de emoción
            cv2.putText(canvas, label, (x+5, y-28),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
            # Texto de confianza
            cv2.putText(canvas, confianza_text, (x+5, y-8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Dibujar barras de probabilidad
            self.dibujar_barras_probabilidad(canvas, prediccion)
        
        return canvas

    def dibujar_barras_probabilidad(self, frame, prediccion):
        """
        Dibuja barras de probabilidad para cada emoción
        """
        x_start = 10
        y_start = 30
        bar_height = 25
        bar_width = 250
        spacing = 35

        for i, emocion in enumerate(self.emociones):
            prob = prediccion[i]
            color = self.colores.get(emocion, (255, 255, 255))
            y_pos = y_start + i * spacing

            # Fondo de la barra
            cv2.rectangle(frame, (x_start, y_pos),
                         (x_start + bar_width, y_pos + bar_height),
                         (40, 40, 40), -1)

            # Barra de probabilidad
            filled_width = int(prob * bar_width)
            cv2.rectangle(frame, (x_start, y_pos),
                         (x_start + filled_width, y_pos + bar_height),
                         color, -1)

            # Borde de la barra
            cv2.rectangle(frame, (x_start, y_pos),
                         (x_start + bar_width, y_pos + bar_height),
                         (200, 200, 200), 2)

            # Texto
            emoji = self.emojis.get(emocion, '')
            text = f"{emoji} {emocion}: {prob*100:.0f}%"
            cv2.putText(frame, text, (x_start + 260, y_pos + 18),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def ejecutar(self):
        """
        Función principal - Detección en tiempo real
        """
        # Abrir cámara
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ ERROR: No se puede acceder a la cámara")
            print("👉 Verifica que la cámara esté conectada")
            return

        # Configuración de cámara
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)

        print("🟢 SISTEMA ACTIVO")
        print("💡 Detector estabilizado y optimizado")
        print("⌨️  Presiona 'Q' para salir")
        print("⌨️  Presiona 'R' para resetear historial\n")

        fps_counter = 0
        fps_time = cv2.getTickCount()
        fps = 0.0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Error al capturar frame")
                break
            
            # Espejo
            frame = cv2.flip(frame, 1)
            
            # Detectar rostros
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostros = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            # Limpiar historial si no hay rostros
            if len(rostros) == 0:
                self.historial_predicciones.clear()
                self.ultima_emocion = None

            # Procesar rostros (solo el más grande)
            rostros_info = []
            rostros_ordenados = sorted(rostros, key=lambda x: x[2]*x[3], reverse=True)
            
            for (x, y, w, h) in rostros_ordenados[:1]:
                roi = frame[y:y+h, x:x+w]
                emocion, confianza, prediccion = self.predecir_emocion(roi)
                
                if emocion is not None:
                    rostros_info.append({
                        'bbox': (x, y, w, h),
                        'emocion': emocion,
                        'confianza': confianza,
                        'prediccion': prediccion
                    })

            # Dibujar interfaz
            canvas = self.dibujar_interfaz(frame, rostros_info)

            # Calcular FPS
            fps_counter += 1
            if fps_counter >= 30:
                fps_time_new = cv2.getTickCount()
                fps = 30 / ((fps_time_new - fps_time) / cv2.getTickFrequency())
                fps_time = fps_time_new
                fps_counter = 0

            # Mostrar FPS
            cv2.putText(canvas, f"FPS: {fps:.1f}", (10, canvas.shape[0]-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Mostrar ventana
            cv2.imshow('Detector de Emociones - 4 Clases', canvas)

            # Controles de teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.historial_predicciones.clear()
                self.ultima_emocion = None
                print("🔄 Historial reseteado")

        cap.release()
        cv2.destroyAllWindows()
        print("\n🔴 Sistema cerrado correctamente")

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 INICIANDO DETECTOR DE EMOCIONES")
    print("="*70 + "\n")
    
    # CONFIGURAR RUTA DEL MODELO
    # Opción 1: Modelo en carpeta específica
    RUTA_CARPETA = r"C:\Users\torit\OneDrive\Escritorio\escuela\IA con Zuriel\Modulo4\Proyecto"
    
    # Opción 2: Modelo en directorio actual
    RUTA_ACTUAL = os.getcwd()
    
    # Buscar modelo
    modelo_encontrado = None
    
    # Buscar en carpeta específica
    if os.path.exists(RUTA_CARPETA):
        archivos = [f for f in os.listdir(RUTA_CARPETA) if f.endswith('.h5')]
        if archivos:
            modelo_encontrado = os.path.join(RUTA_CARPETA, archivos[0])
            print(f"📂 Modelo encontrado en carpeta: {archivos[0]}")
    
    # Buscar en directorio actual
    if modelo_encontrado is None:
        archivos = [f for f in os.listdir(RUTA_ACTUAL) if f.endswith('.h5')]
        if archivos:
            modelo_encontrado = os.path.join(RUTA_ACTUAL, archivos[0])
            print(f"📂 Modelo encontrado: {archivos[0]}")
    
    # Verificar si se encontró
    if modelo_encontrado is None:
        print("❌ ERROR: No se encontró ningún modelo .h5")
        print("\n👉 SOLUCIONES:")
        print("   1. Entrena el modelo primero")
        print("   2. Coloca el archivo .h5 en:")
        print(f"      {RUTA_CARPETA}")
        print(f"      O en: {RUTA_ACTUAL}")
        sys.exit(1)
    
    print(f"✅ Usando modelo: {modelo_encontrado}\n")
    
    # Iniciar detector
    try:
        detector = DetectorEmociones4Clases(modelo_encontrado)
        detector.ejecutar()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
