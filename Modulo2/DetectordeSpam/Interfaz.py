import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from DataManager import DataManager
from NaiveBayes import NaiveBayes

class Interfaz:
    """
    Clase principal para la interfaz gráfica del detector de spam
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Spam - Naive Bayes")
        self.root.geometry("900x600")  # Ventana más pequeña sin gráficas
        self.root.configure(bg='#f0f0f0')
        
        # Instanciar componentes
        self.data_manager = DataManager()
        self.model = NaiveBayes()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🔍 Detector de Spam con Naive Bayes", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Sección 1: Carga de datos
        self._create_data_section(main_frame)
        
        # Sección 2: Entrenamiento del modelo
        self._create_training_section(main_frame)
        
        # Sección 3: Probador de mensajes
        self._create_testing_section(main_frame)
        
        # Sección 4: Métricas y resultados
        self._create_metrics_section(main_frame)
        
        # Sección 5: Información del dataset
        self._create_info_section(main_frame)
    
    def _create_data_section(self, parent):
        """Crea la sección de carga de datos"""
        data_frame = ttk.LabelFrame(parent, text="1. Cargar Datos", padding="10")
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_frame = ttk.Frame(data_frame)
        file_frame.pack(fill=tk.X)
        
        ttk.Label(file_frame, text="Ruta del archivo CSV:").pack(side=tk.LEFT, padx=(0, 10))
        self.file_path = tk.StringVar(value="spam.csv")
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(file_frame, text="Examinar", command=self._browse_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="Cargar Datos", command=self._load_data).pack(side=tk.LEFT)
        
        self.data_status = ttk.Label(data_frame, text="No se han cargado datos", foreground="red")
        self.data_status.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_training_section(self, parent):
        """Crea la sección de entrenamiento del modelo"""
        train_frame = ttk.LabelFrame(parent, text="2. Entrenar Modelo", padding="10")
        train_frame.pack(fill=tk.X, pady=(0, 10))
        
        train_buttons = ttk.Frame(train_frame)
        train_buttons.pack(fill=tk.X)
        
        ttk.Button(train_buttons, text="Entrenar Modelo Naive Bayes", 
                  command=self._train_model).pack(side=tk.LEFT)
        
        self.train_status = ttk.Label(train_buttons, text="Modelo no entrenado")
        self.train_status.pack(side=tk.LEFT, padx=(20, 0))
    
    def _create_testing_section(self, parent):
        """Crea la sección de prueba de mensajes"""
        test_frame = ttk.LabelFrame(parent, text="3. Probar Mensaje", padding="10")
        test_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(test_frame, text="Ingresa un mensaje para clasificar:").pack(anchor=tk.W)
        
        self.message_text = scrolledtext.ScrolledText(test_frame, height=4)
        self.message_text.pack(fill=tk.X, pady=(5, 10))
        
        test_buttons = ttk.Frame(test_frame)
        test_buttons.pack(fill=tk.X)
        
        ttk.Button(test_buttons, text="Clasificar Mensaje", 
                  command=self._classify_message).pack(side=tk.LEFT)
        
        self.result_label = ttk.Label(test_buttons, text="", font=('Arial', 12, 'bold'))
        self.result_label.pack(side=tk.LEFT, padx=(20, 0))
    
    def _create_metrics_section(self, parent):
        """Crea la sección de métricas (sin gráficas)"""
        metrics_frame = ttk.LabelFrame(parent, text="4. Métricas del Modelo", padding="10")
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(metrics_frame, text="Resultados de la evaluación:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, height=8)
        self.metrics_text.pack(fill=tk.X, pady=(5, 0))
    
    def _create_info_section(self, parent):
        """Crea la sección de información del dataset"""
        info_frame = ttk.LabelFrame(parent, text="5. Información del Dataset", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6)
        self.info_text.pack(fill=tk.BOTH, expand=True)
    
    def _browse_file(self):
        """Abre el diálogo para seleccionar archivo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
    
    def _load_data(self):
        """Maneja la carga de datos"""
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor ingresa una ruta de archivo")
            return
        
        success, message = self.data_manager.load_data(file_path)
        
        if success:
            self.data_status.config(text=f"Datos cargados: {len(self.data_manager.data)} registros", 
                                  foreground="green")
            self._show_dataset_info()
        else:
            messagebox.showerror("Error", message)
            self.data_status.config(text="Error al cargar datos", foreground="red")
    
    def _show_dataset_info(self):
        """Muestra información del dataset en la interfaz"""
        info = self.data_manager.get_dataset_info()
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def _train_model(self):
        """Maneja el entrenamiento del modelo"""
        if self.data_manager.data is None:
            messagebox.showerror("Error", "Primero debe cargar los datos")
            return
        
        try:
            self.train_status.config(text="Entrenando modelo...")
            self.root.update()
            
            # Entrenar modelo
            success, message = self.model.train(self.data_manager.data)
            
            if success:
                # Evaluar modelo
                evaluation_results = self.model.evaluate_model(self.data_manager.data)
                self._show_metrics(evaluation_results)
                self.train_status.config(text="Modelo entrenado exitosamente")
            else:
                messagebox.showerror("Error", message)
                self.train_status.config(text="Error en el entrenamiento")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el entrenamiento: {str(e)}")
            self.train_status.config(text="Error en el entrenamiento")
    
    def _show_metrics(self, evaluation_results):
        """Muestra las métricas en la interfaz (sin gráficas)"""
        manual_metrics = evaluation_results['manual']
        sklearn_metrics = evaluation_results['sklearn']
        
        metrics_text = f"""MÉTRICAS DEL MODELO
========================

NAIVE BAYES MANUAL:
-------------------
• Exactitud: {manual_metrics['accuracy']:.2%}
• Precisión: {manual_metrics['precision']:.2%}
• Sensibilidad: {manual_metrics['recall']:.2%}
• Puntuación F1: {manual_metrics['f1']:.2%}

SCI-KIT LEARN:
--------------
• Exactitud: {sklearn_metrics['accuracy']:.2%}
• Precisión: {sklearn_metrics['precision']:.2%}
• Sensibilidad: {sklearn_metrics['recall']:.2%}
• Puntuación F1: {sklearn_metrics['f1']:.2%}

RESUMEN:
--------
El modelo manual tiene una exactitud del {manual_metrics['accuracy']:.2%}
comparado con {sklearn_metrics['accuracy']:.2%} de Scikit-learn.
"""
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(1.0, metrics_text)
    
    def _classify_message(self):
        """Clasifica un mensaje ingresado por el usuario"""
        if not self.model.is_trained:
            messagebox.showerror("Error", "Primero debe entrenar el modelo")
            return
        
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Advertencia", "Por favor ingresa un mensaje para clasificar")
            return
        
        try:
            # Clasificar mensaje
            result = self.model.predict(message)
            
            # Mostrar resultado en la interfaz
            if result['is_spam']:
                self.result_label.config(text="🔴 SPAM DETECTADO", foreground="red")
                result_text = f"""🔴 SPAM DETECTADO

Probabilidad de spam: {result['probability_spam']:.2%}
Probabilidad de no spam: {result['probability_ham']:.2%}

El mensaje ha sido clasificado como SPAM con una probabilidad del {result['probability_spam']:.2%}"""
            else:
                self.result_label.config(text="✅ MENSAJE LEGÍTIMO", foreground="green")
                result_text = f"""✅ MENSAJE LEGÍTIMO

Probabilidad de spam: {result['probability_spam']:.2%}
Probabilidad de no spam: {result['probability_ham']:.2%}

El mensaje ha sido clasificado como LEGÍTIMO con una probabilidad del {result['probability_ham']:.2%}"""
            
            messagebox.showinfo("Resultado de Clasificación", result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al clasificar mensaje: {str(e)}")