Detector de Spam con Naive Bayes

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Machine%2520Learning-Naive%2520Bayes-orange
https://img.shields.io/badge/GUI-Tkinter-green
https://img.shields.io/badge/License-MIT-lightgrey

Sistema inteligente de clasificación de mensajes spam/ham implementado con el algoritmo Naive Bayes

Características • Instalación • Uso • Estructura • Documentación


Tabla de Contenidos
Descripción

Características

Instalación

Uso

Documentación Técnica

Contribución

Licencia

Descripción
Este proyecto implementa un sistema de detección de spam utilizando el algoritmo Naive Bayes. El sistema es capaz de clasificar mensajes de texto en dos categorías: spam (correo no deseado) o ham (correo legítimo). La aplicación incluye una interfaz gráfica intuitiva desarrollada con Tkinter.

Características
Funcionalidades Principales
Carga de Datos: Soporte para archivos CSV con detección automática de codificación

Entrenamiento Dual: Implementación manual + Scikit-learn para comparación

Clasificación en Tiempo Real: Análisis instantáneo de mensajes

Métricas Detalladas: Exactitud, precisión, sensibilidad y F1-score

Probabilidades: Muestra las probabilidades de clasificación

Preprocesamiento Automático: Limpieza y preparación de datos

Características Técnicas
Algoritmo: Naive Bayes Multinomial

Vectorización: TF-IDF con 5000 características

Preprocesamiento: Eliminación de stop words en inglés

Evaluación: Validación con 80-20 split estratificado

Interfaz: Tkinter con diseño responsive

Instalación
Prerrequisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Instalación Paso a Paso
Clonar el repositorio

bash
git clone https://github.com/tu-usuario/detector-spam.git
cd detector-spam
Crear un entorno virtual (recomendado)

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instalar dependencias

bash
pip install -r requirements.txt
requirements.txt
txt
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.0.0
chardet>=5.0.0
Uso
Ejecución de la Aplicación
bash
python main.py
Guía de Uso Paso a Paso
1. Cargar Datos
Haz clic en "Examinar" y selecciona tu archivo CSV

El archivo debe tener al menos 2 columnas: etiqueta y texto

Formato esperado:

csv
etiqueta,texto
spam,"Win a free iPhone now! Click here"
ham,"Hello, how are you doing today?"
2. Entrenar Modelo
Haz clic en "Entrenar Modelo Naive Bayes"

El sistema procesará los datos y entrenará dos modelos:

Naive Bayes Manual: Nuestra implementación

Scikit-learn: Implementación de referencia

3. Clasificar Mensajes
Escribe un mensaje en el área de texto

Haz clic en "Clasificar Mensaje"

Verás el resultado inmediatamente

Ejemplos de Mensajes para Probar
SPAM:

text
Congratulations! You've won a $1000 Walmart gift card. Text STOP to end.
FREE entry into our £250 weekly draw just text SPAM to 80038
Urgent! Your account has been compromised. Click here to secure it.
HAM:

text
Hi John, are we still meeting for lunch tomorrow?
Your package has been delivered. Tracking number: 123456789
Reminder: Doctor's appointment at 3 PM today.

Descripción de Archivos
Archivo	Descripción
main.py	Inicializa y ejecuta la aplicación
data_manager.py	Carga, limpia y preprocesa los datos
naive_bayes_model.py	Implementa el algoritmo de clasificación
gui.py	Interfaz gráfica con Tkinter
Documentación Técnica
Algoritmo Naive Bayes
Fundamentos Matemáticos
El clasificador Naive Bayes se basa en el teorema de Bayes:

text
P(Spam|Mensaje) = P(Mensaje|Spam) * P(Spam) / P(Mensaje)
Donde:

P(Spam|Mensaje): Probabilidad posterior de que sea spam

P(Mensaje|Spam): Verosimilitud del mensaje dado que es spam

P(Spam): Probabilidad previa de spam

P(Mensaje): Evidencia (constante de normalización)

Implementación
python
# Cálculo de probabilidades logarítmicas
log_prob_spam = np.log(P_spam) + np.sum(np.log(P_caracteristicas_spam) * mensaje_vector)
log_prob_ham = np.log(P_ham) + np.sum(np.log(P_caracteristicas_ham) * mensaje_vector)
Preprocesamiento de Datos
Limpieza de Texto

Conversión a minúsculas

Eliminación de espacios en blanco

Filtrado de stop words

Vectorización TF-IDF

Máximo 5000 características

Ponderación por frecuencia inversa

Matriz dispersa eficiente

Métricas de Evaluación
Métrica	Fórmula	Descripción
Exactitud	(TP + TN) / Total	Porcentaje de clasificaciones correctas
Precisión	TP / (TP + FP)	Calidad de las predicciones positivas
Sensibilidad	TP / (TP + FN)	Capacidad de detectar casos positivos
F1-Score	2 * (P * R) / (P + R)	Media armónica de precisión y sensibilidad
Contribución
¡Las contribuciones son bienvenidas! Sigue estos pasos:

Fork el proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

Guía de Estilo de Código
Usa docstrings para documentar funciones y clases

Sigue PEP 8 para estilo de código

Incluye tests para nuevas funcionalidades

Mantén la cobertura de código

Testing
Ejecuta los tests con:

bash
python -m pytest tests/
Cobertura de Tests
bash
python -m pytest --cov=src tests/
Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

Autores
Tu Nombre - Desarrollo inicial - TuUsuario

Agradecimientos
Algoritmo Naive Bayes basado en el libro "Pattern Recognition and Machine Learning"

Dataset de ejemplo del repositorio UCI Machine Learning

Comunidad de Scikit-learn por su implementación de referencia

