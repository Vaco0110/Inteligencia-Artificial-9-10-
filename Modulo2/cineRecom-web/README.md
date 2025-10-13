CineRecom - Sistema de Recomendación de Películas

Integrantes
Jesus Hector Roman Vizar 
Jose Humberto Guitierrez Beltran


https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/Flask-2.3+-green.svg
https://img.shields.io/badge/scikit--learn-1.3+-orange.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Un sistema inteligente de recomendación de películas basado en contenido, implementado como una aplicación web moderna utilizando Flask y algoritmos de machine learning.

Tabla de Contenidos
Características

Demo

Instalación

Uso

API Reference

Desarrollo

Tecnologías Utilizadas

Contribución


Características
Recomendaciones Basadas en Contenido: Encuentra películas similares basándose en sus géneros

Interfaz Moderna: Diseño responsive y amigable con el usuario

Algoritmo Avanzado: Utiliza TF-IDF y similitud coseno para recomendaciones precisas

Base de Datos Integrada: Dataset pre-cargado con 20 películas populares

Diseño Responsive: Compatible con dispositivos móviles y desktop

Demo
https://via.placeholder.com/800x400.png?text=CineRecom+Interface+Demo

Características principales de la interfaz:

Selección intuitiva de películas de referencia

Configuración del número de recomendaciones

Visualización en tiempo real de resultados

Indicadores de similitud porcentual

Diseño con gradientes y animaciones suaves

Instalación
Prerrequisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Git

Pasos de Instalación
Clonar el repositorio

bash
git clone https://github.com/tuusuario/cineRecom.git
cd cineRecom
Crear un entorno virtual (recomendado)

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instalar dependencias

bash
pip install -r requirements.txt
Ejecutar la aplicación

bash
python app.py
Abrir en el navegador

text
http://localhost:5000
Instalación Rápida (Docker)
bash
# Próximamente - Estamos trabajando en la containerización
Uso
Uso Básico
Seleccionar Película de Referencia

Elige una película de la lista desplegable

Por defecto: "The Dark Knight"

Configurar Número de Recomendaciones

Establece cuántas películas similares deseas ver (1-20)

Valor por defecto: 5

Generar Recomendaciones

Haz clic en "Generar Recomendaciones"

El sistema procesará y mostrará los resultados

Interpretación de Resultados
Los resultados incluyen:

Título de la película: Nombre de la película recomendada

Géneros: Lista de géneros de la película

Similitud: Porcentaje de similitud con la película de referencia

Escala de similitud:

80-100%: Muy similar

60-79%: Similar

40-59%: Moderadamente similar

<40%: Poco similar

Algoritmo de Recomendación
El sistema utiliza un enfoque basado en contenido:

Vectorización TF-IDF: Convierte los géneros de las películas en vectores numéricos

Matriz de Similitud: Calcula la similitud coseno entre todos los pares de películas

Ranking: Ordena las películas por similitud con la película de referencia

Filtrado: Excluye la película de referencia y selecciona las N más similares

Fórmula de similitud coseno:

text
sim(A,B) = (A · B) / (||A|| * ||B||)
API Reference
Endpoints Disponibles
GET /
Descripción: Página principal de la aplicación

Respuesta: HTML con la interfaz de usuario

POST /recomendar
Descripción: Genera recomendaciones basadas en una película

Body (JSON):

json
{
  "pelicula": "The Dark Knight",
  "num_recomendaciones": 5
}
Respuesta (JSON):

json
{
  "success": true,
  "recomendaciones": [
    {
      "title": "Inception",
      "genres": "Action|Sci-Fi|Thriller",
      "score": 0.856
    }
  ]
}
Ejemplo de Uso de la API
javascript
// Ejemplo usando fetch
fetch('/recomendar', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        pelicula: 'The Dark Knight',
        num_recomendaciones: 5
    })
})
.then(response => response.json())
.then(data => console.log(data));
🔧 Desarrollo
Configuración del Entorno de Desarrollo
Fork del repositorio

Configurar entorno de desarrollo

bash
git clone https://github.com/tuusuario/cineRecom.git
cd cineRecom
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
Estructura de Datos
Dataset de Películas
python
{
    'movieId': 1,
    'title': 'Titanic',
    'genres': 'Romance|Drama'
}
Dataset de Ratings
python
{
    'userId': 1,
    'movieId': 1,
    'rating': 5
}
Extensión del Sistema
Para agregar nuevas funcionalidades:

Nuevos Algoritmos: Implementar en src/sistema_recomendacion.py

Nuevas Rutas: Agregar en app.py

Nuevas Vistas: Crear plantillas en templates/

Estilos: Modificar static/css/style.css

Tecnologías Utilizadas
Backend
Python 3.8+: Lenguaje de programación principal

Flask 2.3+: Framework web ligero

scikit-learn 1.3+: Machine learning y TF-IDF

pandas 2.0+: Manipulación de datos

numpy 1.24+: Cálculos numéricos

Frontend
HTML5: Estructura web semántica

CSS3: Estilos y animaciones

JavaScript: Interactividad del cliente

Bootstrap 5.1+: Framework CSS responsive

Font Awesome 6.0+: Iconografía

Machine Learning
TF-IDF Vectorization: Conversión de texto a vectores

Cosine Similarity: Cálculo de similitud entre películas

Content-Based Filtering: Algoritmo de recomendación

Contribución
¡Las contribuciones son bienvenidas! Por favor sigue estos pasos:

Fork el proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

Guía de Estilo de Código
Sigue PEP 8 para código Python

Usa nombres descriptivos para variables y funciones

Documenta funciones y clases con docstrings

Mantén el código limpio y organizado


