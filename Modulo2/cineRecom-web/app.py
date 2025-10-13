from flask import Flask, render_template, request, jsonify
from src.Sistema import Sistema

app = Flask(__name__)

# Inicializar sistema
sistema = Sistema()

@app.route('/')
def index():
    """Página principal"""
    peliculas = sistema.df_peliculas['title'].tolist()
    return render_template('index.html', peliculas=peliculas)

@app.route('/recomendar', methods=['POST'])
def recomendar():
    """Endpoint para generar recomendaciones"""
    try:
        data = request.get_json()
        num_recomendaciones = int(data.get('num_recomendaciones', 5))
        pelicula = data.get('pelicula', 'The Dark Knight')
        
        resultados = sistema.recomendacion_basada_contenido(pelicula, num_recomendaciones)
        
        return jsonify({
            'success': True,
            'recomendaciones': resultados
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)