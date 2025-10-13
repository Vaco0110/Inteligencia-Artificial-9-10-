import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Sistema:
    def __init__(self):
        self.df_peliculas = None
        self.df_ratings = None
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar y preparar los datos del dataset"""
        np.random.seed(42)
        
        # Crear dataset de películas
        peliculas_data = {
            'movieId': range(1, 21),
            'title': [
                'Titanic', 'Avatar', 'The Dark Knight', 'Inception', 'Pulp Fiction',
                'Forrest Gump', 'The Matrix', 'The Godfather', 'Fight Club', 'The Shawshank Redemption',
                'Interstellar', 'The Avengers', 'Jurassic Park', 'Star Wars: A New Hope', 'The Lion King',
                'Spirited Away', 'Parasite', 'La La Land', 'Get Out', 'Mad Max: Fury Road'
            ],
            'genres': [
                'Romance|Drama', 'Action|Adventure|Sci-Fi', 'Action|Crime|Drama',
                'Action|Sci-Fi|Thriller', 'Crime|Drama', 'Drama|Romance', 'Action|Sci-Fi',
                'Crime|Drama', 'Drama', 'Drama', 'Adventure|Drama|Sci-Fi', 'Action|Adventure|Sci-Fi',
                'Action|Adventure|Sci-Fi', 'Action|Adventure|Fantasy', 'Animation|Adventure|Drama',
                'Animation|Adventure|Family', 'Comedy|Drama|Thriller', 'Drama|Music|Romance',
                'Horror|Mystery|Thriller', 'Action|Adventure|Sci-Fi'
            ]
        }
        
        # Crear dataset de ratings
        ratings_data = {
            'userId': [],
            'movieId': [],
            'rating': []
        }
        
        # Generar ratings aleatorios
        for user_id in range(1, 51):
            for movie_id in range(1, 21):
                if np.random.random() > 0.7:
                    rating = np.random.choice([3, 4, 5], p=[0.2, 0.5, 0.3])
                    ratings_data['userId'].append(user_id)
                    ratings_data['movieId'].append(movie_id)
                    ratings_data['rating'].append(rating)
        
        self.df_peliculas = pd.DataFrame(peliculas_data)
        self.df_ratings = pd.DataFrame(ratings_data)
    
    def recomendacion_basada_contenido(self, titulo_pelicula, n_recomendaciones=5):
        """Sistema de recomendación basado en contenido"""
        try:
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(self.df_peliculas['genres'])
            
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
            
            idx = self.df_peliculas[self.df_peliculas['title'] == titulo_pelicula].index[0]
            
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:n_recomendaciones+1]
            movie_indices = [i[0] for i in sim_scores]
            
            recomendaciones = self.df_peliculas.iloc[movie_indices][['title', 'genres']].copy()
            recomendaciones['score'] = [sim_scores[i][1] for i in range(len(sim_scores))]
            return recomendaciones.to_dict('records')
        except Exception as e:
            return [{"title": "Error", "genres": f"Película no encontrada: {str(e)}", "score": 0}]