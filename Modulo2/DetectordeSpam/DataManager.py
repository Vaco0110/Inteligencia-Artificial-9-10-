import pandas as pd
import chardet

class DataManager:
   # Clase para manejar la carga y preprocesamiento de datos
    
    def __init__(self):
        self.data = None
        self.encoding = None
    
    def load_data(self, file_path):
        # Carga y procesa el archivo CSV
        try:
            # Detectar codificación
            self._detect_encoding(file_path)
            
            # Leer archivo
            self.data = self._read_csv_with_encoding(file_path)
            
            # Procesar datos
            self._process_data()
            
            return True, "Datos cargados exitosamente"
            
        except Exception as e:
            return False, f"Error al cargar datos: {str(e)}"
    
    def _detect_encoding(self, file_path):
       # Detecta la codificación del archivo
        with open(file_path, 'rb') as f:
            rawdata = f.read(100000)
            self.encoding = chardet.detect(rawdata)['encoding']
    
    def _read_csv_with_encoding(self, file_path):
        # Lee el archivo CSV con la codificación detectada
        try:
            return pd.read_csv(file_path, encoding=self.encoding)
        except UnicodeDecodeError:
            for enc in ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
                try:
                    data = pd.read_csv(file_path, encoding=enc)
                    self.encoding = enc
                    print(f"Usando codificación alternativa: {enc}")
                    return data
                except:
                    continue
            raise ValueError("No se pudo determinar la codificación del archivo")
    
    def _process_data(self):
        # Preprocesa los datos para el análisis
        if len(self.data.columns) >= 2:
            # Tomar las dos primeras columnas y renombrar
            self.data = self.data.iloc[:, :2]
            self.data.columns = ['etiqueta', 'texto']
            
            # Limpiar y convertir etiquetas
            self.data['etiqueta'] = self.data['etiqueta'].astype(str).str.strip().str.lower()
            self.data['spam'] = self.data['etiqueta'].apply(lambda x: 1 if x == 'spam' else 0)
            
            # Eliminar valores nulos
            self.data = self.data.dropna()
            
            # Validar que existan ambas clases
            if self.data['spam'].nunique() < 2:
                raise ValueError("El dataset debe contener ambas clases (spam y no spam)")
        else:
            raise ValueError("El archivo debe contener al menos 2 columnas")
    
    def get_dataset_info(self):
        # Retorna información básica del dataset
        if self.data is None:
            return "No hay datos cargados"
        
        stats = self.get_data_stats()
        
        info = f"""INFORMACIÓN DEL DATASET
----------------------------
Total de registros: {stats['total_records']}
Mensajes spam: {stats['spam_count']} ({stats['spam_ratio']:.1%})
Mensajes no spam: {stats['ham_count']} ({stats['ham_ratio']:.1%})

Primeras 5 filas:
{self.data.head().to_string()}
"""
        return info
    
    def get_data_stats(self):
       # Retorna estadísticas básicas del dataset
        if self.data is None:
            return None
        
        return {
            'total_records': len(self.data),
            'spam_count': self.data['spam'].sum(),
            'ham_count': len(self.data) - self.data['spam'].sum(),
            'spam_ratio': self.data['spam'].mean(),
            'ham_ratio': 1 - self.data['spam'].mean()
        }
    
    def get_data_for_training(self):
        # Retorna los datos preprocesados para entrenamiento
        if self.data is None:
            raise ValueError("No hay datos cargados para entrenamiento")
        return self.data