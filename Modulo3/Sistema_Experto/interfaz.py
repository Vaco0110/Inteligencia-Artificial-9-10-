import logging
import traceback
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import messagebox
from typing import Dict, List

from logica import LogicaProposicional

class InterfazEntrevistaGrafica:
    
    def __init__(self, ventana_raiz: tk.Tk, sistema: LogicaProposicional):
        self.logger = logging.getLogger("InterfazEntrevistaGrafica")
        self.root = ventana_raiz
        self.sistema = sistema
        
        self.root.title("Sistema Experto - Diagnóstico Respiratorio (Modo Inteligente)")
        self.root.geometry("1300x900")  # ← AUMENTADO EL TAMAÑO
        self.root.minsize(1000, 700)   # ← AUMENTADO EL MÍNIMO
        
        self.hechos_conocidos: Dict[str, bool] = {}
        self.preguntas_pendientes: List[str] = []
        self.total_preguntas_posibles: int = 0
        
        # Elementos de la interfaz...
        self.etiqueta_pregunta: ttk.Label = None
        self.marco_botones: ttk.Frame = None
        self.boton_si: ttk.Button = None
        self.boton_no: ttk.Button = None
        self.marco_scroll_resultados: ScrolledFrame = None
        self.texto_explicacion: tk.Text = None
        
        self.marco_progreso: ttk.Frame = None
        self.etiqueta_progreso: ttk.Label = None
        self.barra_progreso: ttk.Progressbar = None
        self.etiqueta_numero_pregunta: ttk.Label = None
        
        self.panel_izquierdo: ttk.Frame = None
        
        self._preparar_preguntas_inteligentes()
        self._inicializar_interfaz()
        self._mostrar_pregunta_siguiente()

    def _preparar_preguntas_inteligentes(self):
        """Prepara la lista inicial de preguntas usando el sistema inteligente"""
        # Obtener las primeras preguntas más importantes
        self.preguntas_pendientes = self.sistema.obtener_primeras_preguntas(10)
        self.total_preguntas_posibles = len(self.sistema.predicados)
        self.logger.info(f"Preparadas {len(self.preguntas_pendientes)} preguntas iniciales de {self.total_preguntas_posibles} posibles.")

    def _inicializar_interfaz(self):
        
        marco_principal = ttk.Frame(self.root, padding="20", bootstyle="light")  # ← MÁS PADDING
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        marco_principal.grid_rowconfigure(0, weight=0)
        marco_principal.grid_rowconfigure(1, weight=1)
        marco_principal.grid_rowconfigure(2, weight=0)
        marco_principal.grid_columnconfigure(0, weight=1)
        
        marco_encabezado = ttk.Frame(marco_principal, bootstyle="primary")
        marco_encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 20))  # ← MÁS ESPACIO
        
        titulo_frame = ttk.Frame(marco_encabezado, bootstyle="primary")
        titulo_frame.pack(fill=tk.X, padx=20, pady=15)
        
        titulo = ttk.Label(
            titulo_frame, 
            text="Sistema Experto de Diagnóstico Respiratorio", 
            font=("Helvetica", 18, "bold"),  # ← FUENTE MÁS PEQUEÑA
            bootstyle="inverse-primary"
        )
        titulo.pack()
        
        subtitulo = ttk.Label(
            titulo_frame,
            text="Sistema adaptativo que hace solo las preguntas más relevantes",
            font=("Helvetica", 10),  # ← FUENTE MÁS PEQUEÑA
            bootstyle="inverse-primary"
        )
        subtitulo.pack(pady=(5, 0))
        
        panel_contenedor = ttk.Frame(marco_principal, bootstyle="light")
        panel_contenedor.grid(row=1, column=0, sticky="nsew")
        
        panel_contenedor.grid_columnconfigure(0, weight=4, minsize=500)  # ← PANEL IZQUIERDO MÁS ANCHO
        panel_contenedor.grid_columnconfigure(1, weight=5, minsize=600)
        panel_contenedor.grid_rowconfigure(0, weight=1)
        
        self.panel_izquierdo = ttk.Frame(panel_contenedor, padding=15, bootstyle="light")  # ← MÁS PADDING
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        card_pregunta = ttk.Frame(self.panel_izquierdo, bootstyle="info", relief="raised")
        card_pregunta.pack(fill=tk.BOTH, expand=True)
        
        header_pregunta = ttk.Frame(card_pregunta, bootstyle="info")
        header_pregunta.pack(fill=tk.X, padx=20, pady=20)  # ← MÁS PADDING
        
        self.etiqueta_numero_pregunta = ttk.Label(
            header_pregunta,
            text="Pregunta 1",
            font=("Helvetica", 12, "bold"),
            bootstyle="inverse-info"
        )
        self.etiqueta_numero_pregunta.pack(anchor="w")
        
        ttk.Separator(card_pregunta, bootstyle="info").pack(fill=tk.X, padx=20)
        
        marco_pregunta_contenedor = ttk.Frame(card_pregunta, height=180)  # ← MÁS ALTO
        marco_pregunta_contenedor.pack(fill=tk.BOTH, expand=True, padx=35, pady=40)  # ← MÁS PADDING
        marco_pregunta_contenedor.pack_propagate(False)
        
        self.etiqueta_pregunta = ttk.Label(
            marco_pregunta_contenedor, 
            text="Cargando pregunta...", 
            font=("Helvetica", 14),  # ← FUENTE MÁS PEQUEÑA
            bootstyle="dark",
            wraplength=450,  # ← MÁS ANCHO PARA TEXTO
            justify="center"
        )
        self.etiqueta_pregunta.pack(expand=True, anchor="center")
        
        self.marco_botones = ttk.Frame(card_pregunta)
        self.marco_botones.pack(fill=tk.X, padx=35, pady=(0, 30))  # ← MÁS PADDING
        
        marco_botones_centrado = ttk.Frame(self.marco_botones)
        marco_botones_centrado.pack(expand=True)
        
        self.boton_no = ttk.Button(
            marco_botones_centrado, 
            text="✗  No", 
            bootstyle="danger-outline",
            width=14,  # ← BOTONES MÁS ANCHOS
            padding=8,  # ← MÁS PADDING
            command=lambda: self._responder(False)
        )
        self.boton_no.pack(side=tk.LEFT, padx=15)  # ← MÁS ESPACIO
        
        self.boton_si = ttk.Button(
            marco_botones_centrado, 
            text="✓  Sí", 
            bootstyle="success",
            width=14,  # ← BOTONES MÁS ANCHOS
            padding=8,  # ← MÁS PADDING
            command=lambda: self._responder(True)
        )
        self.boton_si.pack(side=tk.LEFT, padx=15)  # ← MÁS ESPACIO
        
        self.marco_progreso = ttk.Frame(self.panel_izquierdo, bootstyle="light")
        self.marco_progreso.pack(fill=tk.X, pady=(15, 0))  # ← MÁS ESPACIO
        
        card_progreso = ttk.Frame(self.marco_progreso, bootstyle="secondary", relief="flat")
        card_progreso.pack(fill=tk.X, padx=5, pady=5)
        
        marco_progreso_interno = ttk.Frame(card_progreso)
        marco_progreso_interno.pack(fill=tk.X, padx=20, pady=12)  # ← MÁS PADDING
        
        self.etiqueta_progreso = ttk.Label(
            marco_progreso_interno, 
            text="Progreso: 0/0", 
            font=("Helvetica", 10, "bold"),
            bootstyle="secondary"
        )
        self.etiqueta_progreso.pack(anchor="w")
        
        self.barra_progreso = ttk.Progressbar(
            marco_progreso_interno, 
            bootstyle="success-striped",
            length=350  # ← BARRA MÁS LARGA
        )
        self.barra_progreso.pack(fill=tk.X, pady=(10, 0))
        
        panel_derecho = ttk.Frame(panel_contenedor, padding=15)  # ← MÁS PADDING
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        panel_derecho.grid_rowconfigure(0, weight=3, minsize=300)  # ← MÁS ALTO
        panel_derecho.grid_rowconfigure(1, weight=4, minsize=350)
        panel_derecho.grid_columnconfigure(0, weight=1)
        
        marco_exterior_resultados = ttk.Frame(panel_derecho, bootstyle="light")
        marco_exterior_resultados.grid(row=0, column=0, sticky="nsew", pady=(0, 15))  # ← MÁS ESPACIO
        
        header_resultados = ttk.Frame(marco_exterior_resultados, bootstyle="success")
        header_resultados.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Label(
            header_resultados, 
            text="Diagnósticos Probables", 
            font=("Helvetica", 13, "bold"), 
            bootstyle="inverse-success"
        ).pack(anchor="w", padx=15, pady=10)
        
        self.marco_scroll_resultados = ScrolledFrame(
            marco_exterior_resultados, 
            autohide=True, 
            bootstyle="light"
        )
        self.marco_scroll_resultados.pack(fill=BOTH, expand=True, padx=2, pady=(0, 2))
        
        ttk.Label(
            self.marco_scroll_resultados,
            text="Complete la entrevista para ver los resultados",
            font=("Helvetica", 10, "italic"),
            bootstyle="secondary"
        ).pack(pady=20)
        
        marco_exterior_explicacion = ttk.Frame(panel_derecho, bootstyle="light")
        marco_exterior_explicacion.grid(row=1, column=0, sticky="nsew", pady=(15, 0))  # ← MÁS ESPACIO
        
        header_explicacion = ttk.Frame(marco_exterior_explicacion, bootstyle="info")
        header_explicacion.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Label(
            header_explicacion,
            text="Explicación Detallada",
            font=("Helvetica", 13, "bold"),
            bootstyle="inverse-info"
        ).pack(anchor="w", padx=15, pady=10)
        
        frame_texto = ttk.Frame(marco_exterior_explicacion)
        frame_texto.pack(fill=BOTH, expand=True, padx=2, pady=(0, 2))
        
        self.texto_explicacion = tk.Text(
            frame_texto, 
            wrap="word", 
            relief="flat", 
            font=("Helvetica", 10),
            padx=15,
            pady=10,
            bg="#f8f9fa"
        )
        scrollbar_explicacion = ttk.Scrollbar(
            frame_texto, 
            orient=VERTICAL, 
            command=self.texto_explicacion.yview
        )
        self.texto_explicacion.config(yscrollcommand=scrollbar_explicacion.set)
        
        scrollbar_explicacion.pack(side=RIGHT, fill=Y)
        self.texto_explicacion.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.texto_explicacion.insert(
            "1.0",
            "Seleccione un diagnóstico de la lista para ver su explicación detallada."
        )
        self.texto_explicacion.config(state="disabled")
        
        marco_botones_inferior = ttk.Frame(marco_principal, bootstyle="light")
        marco_botones_inferior.grid(row=2, column=0, sticky="ew", pady=(15, 5))  # ← MÁS ESPACIO
        
        self.boton_reiniciar = ttk.Button(
            marco_botones_inferior, 
            text="Reiniciar Entrevista", 
            command=self._reiniciar_entrevista, 
            bootstyle="warning",
            width=26,
            padding=6
        )
        self.boton_reiniciar.pack(side=tk.RIGHT, padx=12)

    def _actualizar_preguntas_pendientes(self):
        """Actualiza la lista de preguntas pendientes basándose en el diagnóstico actual"""
        diagnosticos_actuales = self.sistema.diagnosticos_probables(umbral=10.0)
        
        if len(diagnosticos_actuales) >= 1:
            # Si ya tenemos diagnósticos probables, enfocarnos en preguntas discriminantes
            nuevas_preguntas = self.sistema.obtener_preguntas_criticas(5)
        else:
            # Si no hay diagnósticos claros, seguir con preguntas generales importantes
            nuevas_preguntas = self.sistema.obtener_primeras_preguntas(5)
        
        # Filtrar preguntas ya respondidas y agregar las nuevas
        nuevas_preguntas = [p for p in nuevas_preguntas if p not in self.hechos_conocidos]
        self.preguntas_pendientes = nuevas_preguntas[:5]  # Limitar a 5 preguntas por lote
        
        # Si no hay más preguntas relevantes, finalizar
        if not self.preguntas_pendientes:
            self._finalizar_entrevista()

    def _actualizar_progreso(self):
        progreso_actual = len(self.hechos_conocidos)
        total = self.total_preguntas_posibles
        

        self.etiqueta_numero_pregunta.config(
            text=f"Pregunta {progreso_actual + 1}"
        )
        
        texto_progreso = f"Progreso: {progreso_actual} / {total} síntomas evaluados"
        self.etiqueta_progreso.config(text=texto_progreso)
        
        if total > 0:
            porcentaje = (progreso_actual / total) * 100
            self.barra_progreso.config(value=porcentaje)
        else:
            self.barra_progreso.config(value=0)

        if not self.preguntas_pendientes and progreso_actual > 0:
            self.etiqueta_progreso.config(text="¡Entrevista Optimizada! ✓")
            self.barra_progreso.config(value=100, bootstyle="success")


            
    def _mostrar_pregunta_siguiente(self):
        self._actualizar_progreso()
        
        if not self.preguntas_pendientes:
            self._finalizar_entrevista()
            return
        
        try:
            predicado_codigo = self.preguntas_pendientes[0]
            descripcion = self.sistema.predicados[predicado_codigo]
            
            # SOLO MOSTRAR LA PREGUNTA, SIN PORCENTAJE DE RELEVANCIA
            texto_pregunta = f"¿{descripcion}?"
            
            self.etiqueta_pregunta.config(text=texto_pregunta)
            
        except (IndexError, KeyError) as e:
            self.logger.error(f"Error al mostrar pregunta: {e}")
            self.preguntas_pendientes.pop(0)
            self._mostrar_pregunta_siguiente()

    def _responder(self, respuesta: bool):
        if not self.preguntas_pendientes:
            return
            
        predicado_codigo = self.preguntas_pendientes.pop(0)
        self.hechos_conocidos[predicado_codigo] = respuesta
        self.sistema.establecer_hecho(predicado_codigo, respuesta)
        
        # Actualizar las preguntas pendientes basándose en las respuestas actuales
        self._actualizar_preguntas_pendientes()
        
        self._mostrar_pregunta_siguiente()

    def _finalizar_entrevista(self):
        self.etiqueta_pregunta.config(
            text="✓ ¡Entrevista optimizada completada!\n\n"
                 f"Se evaluaron {len(self.hechos_conocidos)} síntomas de {self.total_preguntas_posibles} posibles.\n"
                 "Generando diagnóstico final..."
        )
        self.logger.info(f"Entrevista finalizada. Se usaron {len(self.hechos_conocidos)} síntomas de {self.total_preguntas_posibles}")
        
        self.marco_botones.pack_forget()
        
        self._evaluar_diagnosticos()
        self._actualizar_progreso()

    def _reiniciar_entrevista(self):
        self.sistema.respuestas.clear()
        self.hechos_conocidos.clear()
        self._preparar_preguntas_inteligentes()
        
        for widget in self.marco_scroll_resultados.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.marco_scroll_resultados,
            text="Complete la entrevista para ver los resultados",
            font=("Helvetica", 10, "italic"),
            bootstyle="secondary"
        ).pack(pady=20)
        
        self.texto_explicacion.config(state="normal")
        self.texto_explicacion.delete(1.0, tk.END)
        self.texto_explicacion.insert(
            "1.0",
            "Seleccione un diagnóstico de la lista para ver su explicación detallada."
        )
        self.texto_explicacion.config(state="disabled")
        
        self.marco_botones.pack(fill=tk.X, padx=30, pady=(0, 25))
        self.boton_si.config(state="normal")
        self.boton_no.config(state="normal")
        
        self.barra_progreso.config(bootstyle="success-striped")
        
        self._mostrar_pregunta_siguiente()
        self.logger.info("Entrevista reiniciada.")

    # Los métodos _evaluar_diagnosticos y _mostrar_explicacion se mantienen igual
    def _evaluar_diagnosticos(self):
        try:
            for widget in self.marco_scroll_resultados.winfo_children():
                widget.destroy()
            
            diagnosticos = self.sistema.diagnosticos_probables(umbral=10.0)
            
            if not diagnosticos:
                marco_no_resultados = ttk.Frame(self.marco_scroll_resultados)
                marco_no_resultados.pack(fill=tk.X, pady=20, padx=15)
                
                ttk.Label(
                    marco_no_resultados,
                    text="⚠️ No hay diagnósticos que cumplan con el umbral mínimo",
                    font=("Helvetica", 11),
                    bootstyle="warning"
                ).pack()
                return
            
            for i, (enfermedad, probabilidad) in enumerate(diagnosticos):
                card_resultado = ttk.Frame(
                    self.marco_scroll_resultados,
                    bootstyle="light",
                    relief="raised"
                )
                card_resultado.pack(fill=tk.X, pady=8, padx=10)
                
                contenido_card = ttk.Frame(card_resultado)
                contenido_card.pack(fill=tk.X, padx=15, pady=12)
                
                fila_superior = ttk.Frame(contenido_card)
                fila_superior.pack(fill=tk.X, pady=(0, 8))
                
                boton_explicar = ttk.Button(
                    fila_superior, 
                    text=f"{enfermedad}",
                    command=lambda e=enfermedad: self._mostrar_explicacion(e),
                    bootstyle="info-link",
                    cursor="hand2"
                )
                boton_explicar.pack(side=tk.LEFT)
                
                if probabilidad >= 99.9:
                    badge = ttk.Label(
                        fila_superior,
                        text="DIAGNÓSTICO PRINCIPAL",
                        bootstyle="success",
                        font=("Helvetica", 8, "bold")
                    )
                    badge.pack(side=tk.RIGHT, padx=5)
                
                fila_inferior = ttk.Frame(contenido_card)
                fila_inferior.pack(fill=tk.X)
                
                if probabilidad >= 80:
                    color_barra = "success"
                elif probabilidad >= 50:
                    color_barra = "warning"
                else:
                    color_barra = "info"
                
                barra_progreso = ttk.Progressbar(
                    fila_inferior, 
                    orient=tk.HORIZONTAL, 
                    length=250, 
                    value=probabilidad,
                    bootstyle=color_barra
                )
                barra_progreso.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
                
                etiqueta_porcentaje = ttk.Label(
                    fila_inferior,
                    text=f"{probabilidad:.1f}%",
                    font=("Helvetica", 11, "bold"),
                    bootstyle=color_barra
                )
                etiqueta_porcentaje.pack(side=tk.RIGHT)
            
            if diagnosticos:
                self._mostrar_explicacion(diagnosticos[0][0])
                
        except Exception as e:
            self.logger.error(f"Error al evaluar diagnósticos: {e}")
            self.logger.error(traceback.format_exc())
            messagebox.showerror("Error", f"Error al evaluar diagnósticos: {str(e)}")
    
    def _mostrar_explicacion(self, enfermedad):
        try:
            explicacion = self.sistema.explicar_diagnostico(enfermedad)
            
            self.texto_explicacion.config(state="normal")
            self.texto_explicacion.delete(1.0, tk.END)
            
            self.texto_explicacion.insert(tk.END, f"🩺 DIAGNÓSTICO: {enfermedad}\n", "titulo")
            self.texto_explicacion.insert(tk.END, f"Probabilidad: {explicacion['probabilidad']:.1f}%\n", "probabilidad")
            self.texto_explicacion.insert(tk.END, "\n" + "─" * 50 + "\n\n", "separador")
            
            self.texto_explicacion.insert(tk.END, "📐 Fórmula Lógica:\n", "subtitulo")
            self.texto_explicacion.insert(tk.END, f"{explicacion['formula_logica']}\n\n", "formula")
            self.texto_explicacion.insert(tk.END, "─" * 50 + "\n\n", "separador")
            
            self.texto_explicacion.insert(tk.END, "✓ Factores Presentes (Apoyan el diagnóstico):\n", "subtitulo_verde")
            if explicacion['descripcion_predicados']['req_presentes']:
                for codigo, desc in explicacion['descripcion_predicados']['req_presentes'].items():
                    self.texto_explicacion.insert(tk.END, f"  • {desc}\n", "presente")
            else:
                self.texto_explicacion.insert(tk.END, "  Ninguno\n", "normal")
            
            self.texto_explicacion.insert(tk.END, "\n")
            
            self.texto_explicacion.insert(tk.END, "✗ Factores Ausentes (Deberían estar presentes):\n", "subtitulo_rojo")
            if explicacion['descripcion_predicados']['req_ausentes']:
                for codigo, desc in explicacion['descripcion_predicados']['req_ausentes'].items():
                    self.texto_explicacion.insert(tk.END, f"  • {desc}\n", "ausente")
            else:
                self.texto_explicacion.insert(tk.END, "  Ninguno\n", "normal")
            
            self.texto_explicacion.insert(tk.END, "\n")
            
            self.texto_explicacion.insert(tk.END, "✓ Factores Correctamente Ausentes:\n", "subtitulo_verde")
            if explicacion['descripcion_predicados']['excl_cumplidos']:
                for codigo, desc in explicacion['descripcion_predicados']['excl_cumplidos'].items():
                    self.texto_explicacion.insert(tk.END, f"  • {desc}\n", "presente")
            else:
                self.texto_explicacion.insert(tk.END, "  Ninguno\n", "normal")
            
            self.texto_explicacion.insert(tk.END, "\n")
            
            self.texto_explicacion.insert(tk.END, "⚠ Factores que Contradicen el Diagnóstico:\n", "subtitulo_amarillo")
            if explicacion['descripcion_predicados']['excl_incumplidos']:
                for codigo, desc in explicacion['descripcion_predicados']['excl_incumplidos'].items():
                    self.texto_explicacion.insert(tk.END, f"  • {desc}\n", "contradice")
            else:
                self.texto_explicacion.insert(tk.END, "  Ninguno\n", "normal")
            
            self.texto_explicacion.tag_configure("titulo", font=("Helvetica", 14, "bold"), foreground="#0d6efd")
            self.texto_explicacion.tag_configure("probabilidad", font=("Helvetica", 12, "bold"), foreground="#198754")
            self.texto_explicacion.tag_configure("separador", foreground="#6c757d")
            self.texto_explicacion.tag_configure("subtitulo", font=("Helvetica", 11, "bold"), foreground="#0dcaf0")
            self.texto_explicacion.tag_configure("subtitulo_verde", font=("Helvetica", 11, "bold"), foreground="#198754")
            self.texto_explicacion.tag_configure("subtitulo_rojo", font=("Helvetica", 11, "bold"), foreground="#dc3545")
            self.texto_explicacion.tag_configure("subtitulo_amarillo", font=("Helvetica", 11, "bold"), foreground="#ffc107")
            self.texto_explicacion.tag_configure("formula", font=("Courier", 9, "italic"), foreground="#6c757d", background="#f8f9fa")
            self.texto_explicacion.tag_configure("presente", foreground="#198754", font=("Helvetica", 10))
            self.texto_explicacion.tag_configure("ausente", foreground="#dc3545", font=("Helvetica", 10))
            self.texto_explicacion.tag_configure("contradice", foreground="#fd7e14", font=("Helvetica", 10))
            self.texto_explicacion.tag_configure("normal", foreground="#6c757d", font=("Helvetica", 10, "italic"))
            
            self.texto_explicacion.config(state="disabled")
            
        except Exception as e:
            self.logger.error(f"Error al mostrar explicación: {e}")
            self.logger.error(traceback.format_exc())
            messagebox.showerror("Error", f"Error al mostrar explicación: {str(e)}")