Sistema Experto de Diagnóstico Respiratorio
#Descripción
El Sistema Experto de Diagnóstico Respiratorio es una aplicación desarrollada en Python que utiliza lógica proposicional y una interfaz gráfica moderna para asistir en el diagnóstico de enfermedades respiratorias. El sistema emplea un enfoque de preguntas inteligentes y adaptativas para llegar a conclusiones de manera eficiente.

#Características Principales
Sistema de Preguntas Inteligente
Priorización automática de síntomas más relevantes

Preguntas adaptativas que se ajustan según las respuestas del usuario

Enfoque discriminante para diferenciar entre diagnósticos probables

Optimización del proceso con menos preguntas necesarias

Base de Conocimiento Completa
25 enfermedades respiratorias diferentes

46 síntomas y signos clínicos evaluados

Reglas lógicas precisas para cada diagnóstico

Cobertura amplia desde resfriados comunes hasta condiciones graves

Interfaz Moderna y Usable
Diseño responsive con ttkbootstrap

Panel de explicaciones detalladas para cada diagnóstico

Barra de progreso visual

Resultados ordenados por probabilidad

Librerías Utilizadas
Librerías Principales
ttkbootstrap - Interfaz gráfica moderna y temática

tkinter - Framework base para la interfaz gráfica

json - Manejo de la base de conocimiento

logging - Sistema de registro de eventos

pathlib - Manejo de rutas de archivos

Librerías Estándar
typing - Tipado de datos para mejor desarrollo

sys - Funcionalidades del sistema

traceback - Manejo de errores detallado

Instalación y Ejecución
Prerrequisitos
Python 3.7 o superior

pip (gestor de paquetes de Python)

Pasos para Ejecutar
Clonar o descargar los archivos del proyecto:

text
main.py
logica.py
interfaz.py
base_de_conocimiento.json
Instalar las dependencias necesarias:

bash
pip install ttkbootstrap
Ejecutar la aplicación:

bash
python main.py
Verificar que todos los archivos estén en la misma carpeta

Cómo Funciona el Sistema
Arquitectura del Sistema
1. Base de Conocimiento (base_de_conocimiento.json)
Predicados: Síntomas y signos clínicos codificados

Reglas: Condiciones lógicas para cada enfermedad

Estructura lógica: Sistema de requeridos y excluidos

2. Motor de Inferencia (logica.py)
Evaluación de reglas lógicas proposicionales

Cálculo de probabilidades basado en síntomas presentes/ausentes

Sistema de priorización de preguntas

Explicaciones detalladas de diagnósticos

3. Interfaz de Usuario (interfaz.py)
Entrevista guiada adaptativa

Visualización de resultados en tiempo real

Panel de explicaciones interactivo

Algoritmo de Diagnóstico
Inicialización: Carga la base de conocimiento

Selección de Preguntas: Elige los síntomas más discriminantes

Evaluación Continua: Recalcula diagnósticos probables después de cada respuesta

Refinamiento: Enfoca en síntomas que diferencian entre diagnósticos principales

Conclusión: Presenta resultados ordenados por probabilidad

Tutorial de Uso
Paso 1: Inicio de la Aplicación
Ejecute python main.py

La ventana principal se abrirá con el título "Sistema Experto de Diagnóstico Respiratorio"

Paso 2: Responder las Preguntas
Lea cuidadosamente cada pregunta sobre síntomas

Responda con veracidad usando los botones "Sí" o "No"

Observe el progreso en la barra inferior

El sistema hará menos preguntas gracias a su inteligencia adaptativa

Paso 3: Revisar Resultados
Los diagnósticos aparecen automáticamente al finalizar

Cada enfermedad muestra su probabilidad en porcentaje

Las barras de colores indican el nivel de certeza:

Verde (>=80%): Alta probabilidad

Amarillo (50-79%): Probabilidad media

Azul (<50%): Baja probabilidad

Paso 4: Analizar Explicaciones
Haga clic en cualquier diagnóstico para ver detalles

Revise los factores que apoyan o contradicen el diagnóstico

Considere la fórmula lógica utilizada para el razonamiento

Paso 5: Reiniciar (Opcional)
Use el botón "Reiniciar Entrevista" para comenzar de nuevo

Todos los datos previos se limpiarán

Ejemplo de Uso
Caso Clínico Ejemplo
Usuario presenta:

Fiebre alta (>38.5°C)

Tos seca

Malestar general intenso

Pérdida del olfato/gusto

Proceso del Sistema:

Pregunta sobre fiebre alta 

Pregunta sobre tos seca 

Pregunta sobre malestar general 

Pregunta sobre pérdida olfato 

El sistema detecta patrón COVID-19 y hace preguntas específicas

Resultado Final:
COVID-19 - 95% de probabilidad

Influenza - 45% de probabilidad

Resfriado Común - 15% de probabilidad

Estructura del Proyecto
text
sistema-experto-respiratorio/
│
├── main.py                 # Punto de entrada de la aplicación
├── logica.py              # Motor de inferencia lógica
├── interfaz.py            # Interfaz gráfica de usuario
├── base_de_conocimiento.json # Base de conocimiento médica
└── sistema_experto.log    # Archivo de log (generado automáticamente)
