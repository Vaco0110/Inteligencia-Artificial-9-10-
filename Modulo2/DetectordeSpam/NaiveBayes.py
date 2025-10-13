import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class NaiveBayes:
   
    
    def __init__(self):
        self.vectorizer = None
        self.P_spam = 0
        self.P_ham = 0
        self.P_caracteristicas_spam = None
        self.P_caracteristicas_ham = None
        self.features_array = None
        self.sklearn_model = None
        self.is_trained = False
    
    def train(self, data):
        # Entrena el modelo Naive Bayes manualmente
        try:
            # Preparar características con TF-IDF
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
            features = self.vectorizer.fit_transform(data["texto"])
            self.features_array = features.toarray()
            
            # Calcular probabilidades previas
            self.P_spam = data["spam"].sum() / len(data)
            self.P_ham = 1 - self.P_spam
            
            # Calcular probabilidades condicionales
            P_caracteristicas_spam = self.features_array[data["spam"] == 1].sum(axis=0) / self.features_array[data["spam"] == 1].sum()
            P_caracteristicas_ham = self.features_array[data["spam"] == 0].sum(axis=0) / self.features_array[data["spam"] == 0].sum()
            
            # Evitar problemas numéricos
            self.P_caracteristicas_spam = np.clip(P_caracteristicas_spam, 1e-10, 1)
            self.P_caracteristicas_ham = np.clip(P_caracteristicas_ham, 1e-10, 1)
            
            self.is_trained = True
            return True, "Modelo entrenado exitosamente"
            
        except Exception as e:
            self.is_trained = False
            return False, f"Error en el entrenamiento: {str(e)}"
    
    def predict(self, message):
        # Realiza una predicción para un mensaje dado
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Vectorizar mensaje
        message_vector = self.vectorizer.transform([message]).toarray()
        
        # Calcular log-probabilidades
        log_prob_spam = np.log(self.P_spam) + np.sum(np.log(self.P_caracteristicas_spam) * message_vector, axis=1)
        log_prob_ham = np.log(self.P_ham) + np.sum(np.log(self.P_caracteristicas_ham) * message_vector, axis=1)
        
        # Determinar clase y calcular probabilidades
        is_spam = log_prob_spam > log_prob_ham
        prob_spam = np.exp(log_prob_spam) / (np.exp(log_prob_spam) + np.exp(log_prob_ham))
        prob_ham = np.exp(log_prob_ham) / (np.exp(log_prob_spam) + np.exp(log_prob_ham))
        
        return {
            'is_spam': bool(is_spam[0]),
            'probability_spam': float(prob_spam[0]),
            'probability_ham': float(prob_ham[0]),
            'log_prob_spam': float(log_prob_spam[0]),
            'log_prob_ham': float(log_prob_ham[0])
        }
    
    def evaluate_model(self, data):
        # Evalúa el modelo comparando con Scikit-learn
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            self.features_array, data["spam"], test_size=0.2, random_state=42, stratify=data["spam"]
        )
        
        # Naive Bayes manual
        y_pred_manual = self._predict_batch(X_test)
        
        # Scikit-learn
        self.sklearn_model = MultinomialNB()
        self.sklearn_model.fit(X_train, y_train)
        y_pred_sklearn = self.sklearn_model.predict(X_test)
        
        # Calcular métricas
        manual_metrics = self._calculate_metrics(y_test, y_pred_manual)
        sklearn_metrics = self._calculate_metrics(y_test, y_pred_sklearn)
        
        return {
            'manual': manual_metrics,
            'sklearn': sklearn_metrics,
            'y_test': y_test,
            'y_pred_manual': y_pred_manual,
            'y_pred_sklearn': y_pred_sklearn
        }
    
    def _predict_batch(self, X):
        # Realiza predicciones en batch usando Naive Bayes manual
        log_prob_spam = np.log(self.P_spam) + np.sum(np.log(self.P_caracteristicas_spam) * X, axis=1)
        log_prob_ham = np.log(self.P_ham) + np.sum(np.log(self.P_caracteristicas_ham) * X, axis=1)
        return (log_prob_spam > log_prob_ham).astype(int)
    
    def _calculate_metrics(self, y_true, y_pred):
        # Calcula métricas de evaluación
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred)
        }
    
    def get_training_info(self):
        # Retorna información del modelo entrenado
        if not self.is_trained:
            return "Modelo no entrenado"
        
        return {
            'P_spam': self.P_spam,
            'P_ham': self.P_ham,
            'vocabulary_size': len(self.vectorizer.get_feature_names_out()) if self.vectorizer else 0,
            'is_trained': self.is_trained
        }