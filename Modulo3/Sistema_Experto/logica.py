import logging
import json
from typing import Dict, List, Tuple, Set


class LogicaProposicional:
    """Sistema de inferencia basado en lógica proposicional para diagnósticos respiratorios"""
    
    def __init__(self, ruta_base_conocimiento: str):
        self.logger = logging.getLogger("LogicaProposicional")
        self.predicados = {}  # Mapeo de código a descripción
        self.respuestas = {}  # Estado actual de los predicados (verdadero/falso)
        self.reglas = {}      # Reglas de inferencia para cada enfermedad
        self.predicados_importancia = {}  # Peso de cada predicado
        
        try:
            self._cargar_base_conocimiento(ruta_base_conocimiento)
            self._calcular_importancia_predicados()
        except Exception as e:
            self.logger.critical(f"Error fatal al cargar la base de conocimiento desde {ruta_base_conocimiento}: {e}")
            raise
    
    def _cargar_base_conocimiento(self, ruta_archivo: str):
        """Carga los predicados y reglas desde un archivo JSON"""
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.predicados = data.get("predicados", {})
        self.reglas = data.get("reglas", {})
        
        if not self.predicados or not self.reglas:
            self.logger.warning("La base de conocimiento está vacía o mal formada.")
            
        self.logger.info(f"Cargados {len(self.predicados)} predicados y {len(self.reglas)} reglas.")

    def _calcular_importancia_predicados(self):
        """Calcula la importancia de cada predicado basado en su frecuencia en las reglas"""
        frecuencia = {}
        for enfermedad, regla in self.reglas.items():
            for pred in regla.get("requeridos", []):
                frecuencia[pred] = frecuencia.get(pred, 0) + 1
            for pred in regla.get("excluidos", []):
                frecuencia[pred] = frecuencia.get(pred, 0) + 1
        
        # Normalizar importancia (0-100)
        max_freq = max(frecuencia.values()) if frecuencia else 1
        for pred, freq in frecuencia.items():
            self.predicados_importancia[pred] = (freq / max_freq) * 100
    
    def establecer_hecho(self, predicado: str, valor: bool) -> None:
        """Establece el valor de verdad de un predicado atómico"""
        if predicado not in self.predicados:
            self.logger.warning(f"Predicado desconocido: {predicado}")
            return
        
        self.respuestas[predicado] = valor
        self.logger.info(f"Establecido predicado {predicado} = {valor}")
    
    def obtener_siguiente_pregunta_optima(self) -> str:
        """
        Devuelve el código del siguiente predicado más importante que no ha sido preguntado,
        priorizando aquellos que pueden descartar más enfermedades rápidamente.
        """
        predicados_no_preguntados = [
            pred for pred in self.predicados 
            if pred not in self.respuestas and pred in self.predicados_importancia
        ]
        
        if not predicados_no_preguntados:
            return None
        
        # Ordenar por importancia descendente
        predicados_no_preguntados.sort(
            key=lambda x: self.predicados_importancia.get(x, 0), 
            reverse=True
        )
        
        return predicados_no_preguntados[0]
    
    def obtener_preguntas_criticas(self, cantidad: int = 5) -> List[str]:
        """
        Devuelve las preguntas más críticas para refinar el diagnóstico actual
        """
        diagnosticos_actuales = self.diagnosticos_probables(umbral=10.0)
        
        if not diagnosticos_actuales:
            return self.obtener_primeras_preguntas(cantidad)
        
        # Encontrar predicados que discriminan entre los diagnósticos principales
        enfermedades_principales = [enf for enf, _ in diagnosticos_actuales[:3]]
        predicados_discriminantes = self._encontrar_predicados_discriminantes(enfermedades_principales)
        
        return predicados_discriminantes[:cantidad]
    
    def _encontrar_predicados_discriminantes(self, enfermedades: List[str]) -> List[str]:
        """Encuentra predicados que diferencian entre las enfermedades dadas"""
        discriminantes = []
        
        for pred in self.predicados:
            if pred in self.respuestas:
                continue
                
            valores_por_enfermedad = []
            for enf in enfermedades:
                regla = self.reglas.get(enf, {})
                # Verificar si este predicado es importante para esta enfermedad
                es_requerido = pred in regla.get("requeridos", [])
                es_excluido = pred in regla.get("excluidos", [])
                
                if es_requerido:
                    valores_por_enfermedad.append(True)
                elif es_excluido:
                    valores_por_enfermedad.append(False)
                else:
                    valores_por_enfermedad.append(None)  # No relevante
            
            # Si el predicado tiene valores diferentes entre enfermedades, es discriminante
            if len(set(valores_por_enfermedad)) > 1:
                discriminantes.append(pred)
        
        # Ordenar por importancia
        discriminantes.sort(key=lambda x: self.predicados_importancia.get(x, 0), reverse=True)
        return discriminantes
    
    def obtener_primeras_preguntas(self, cantidad: int = 5) -> List[str]:
        """Devuelve las primeras preguntas más importantes"""
        todos_predicados = list(self.predicados.keys())
        todos_predicados.sort(key=lambda x: self.predicados_importancia.get(x, 0), reverse=True)
        return [p for p in todos_predicados if p not in self.respuestas][:cantidad]

    # Los métodos existentes se mantienen igual...
    def evaluar_regla(self, enfermedad: str) -> Tuple[bool, float, Dict[str, bool]]:
        """Evalúa una regla lógica para una enfermedad"""
        if enfermedad not in self.reglas:
            self.logger.warning(f"Enfermedad no definida: {enfermedad}")
            return False, 0.0, {}
        
        regla = self.reglas[enfermedad]
        requeridos = regla.get("requeridos", [])
        excluidos = regla.get("excluidos", [])
        
        requeridos_totales = len(requeridos)
        excluidos_totales = len(excluidos)
        total_predicados = requeridos_totales + excluidos_totales
        
        if total_predicados == 0:
            return False, 0.0, {}
        
        # Verificar predicados requeridos (conjunción)
        requeridos_cumplidos = 0
        estado_requeridos = {}
        for pred in requeridos:
            valor = self.respuestas.get(pred, False) # Ausente por defecto es False
            estado_requeridos[pred] = valor
            if valor:
                requeridos_cumplidos += 1
        
        # Verificar predicados excluidos (negación)
        excluidos_cumplidos = 0
        estado_excluidos = {}
        for pred in excluidos:
            # Corrección lógica: Un síntoma no marcado (ausente) es False.
            # not False = True (la condición de exclusión se cumple).
            valor = not self.respuestas.get(pred, False) 
            estado_excluidos[pred] = valor
            if valor:
                excluidos_cumplidos += 1
        
        # Calcular cumplimiento total
        predicados_cumplidos = requeridos_cumplidos + excluidos_cumplidos
        porcentaje = (predicados_cumplidos / total_predicados) * 100 if total_predicados > 0 else 0
        
        # Verificar si se cumple la regla completamente
        regla_cumplida = (requeridos_cumplidos == requeridos_totales and 
                          excluidos_cumplidos == excluidos_totales)
        
        detalles = {
            "requeridos": estado_requeridos,
            "excluidos": estado_excluidos
        }
        
        return regla_cumplida, porcentaje, detalles
    
    def evaluar_todas_reglas(self) -> List[Tuple[str, bool, float, Dict]]:
        """Evalúa todas las reglas y devuelve los resultados ordenados por probabilidad"""
        resultados = []
        
        for enfermedad in self.reglas:
            cumple, porcentaje, detalles = self.evaluar_regla(enfermedad)
            resultados.append((enfermedad, cumple, porcentaje, detalles))
        
        # Ordenar por porcentaje de cumplimiento (descendente)
        resultados.sort(key=lambda x: x[2], reverse=True)
        return resultados
    
    def diagnosticos_probables(self, umbral: float = 30.0) -> List[Tuple[str, float]]:
        """Devuelve las enfermedades que superan cierto umbral de probabilidad"""
        resultados = self.evaluar_todas_reglas()
        diagnosticos = [(enf, porc) for enf, _, porc, _ in resultados if porc >= umbral]
        return diagnosticos
    
    def explicar_diagnostico(self, enfermedad: str) -> Dict:
        """Explica el diagnóstico para una enfermedad específica"""
        _, porcentaje, detalles = self.evaluar_regla(enfermedad)
        
        # Generar explicación
        req_presentes = [p for p, v in detalles["requeridos"].items() if v]
        req_ausentes = [p for p, v in detalles["requeridos"].items() if not v]
        excl_cumplidos = [p for p, v in detalles["excluidos"].items() if v]
        excl_incumplidos = [p for p, v in detalles["excluidos"].items() if not v]
        
        explicacion = {
            "enfermedad": enfermedad,
            "probabilidad": porcentaje,
            "descripcion_predicados": {
                "req_presentes": {p: self.predicados[p] for p in req_presentes},
                "req_ausentes": {p: self.predicados[p] for p in req_ausentes},
                "excl_cumplidos": {p: self.predicados[p] for p in excl_cumplidos},
                "excl_incumplidos": {p: self.predicados[p] for p in excl_incumplidos}
            },
            "formula_logica": self._generar_formula_logica(enfermedad)
        }
        
        return explicacion
    
    def _generar_formula_logica(self, enfermedad: str) -> str:
        """Genera la fórmula lógica para una enfermedad"""
        regla = self.reglas.get(enfermedad, {})
        requeridos_str = " ∧ ".join([f"{p}" for p in regla.get("requeridos", [])])
        excluidos_str = " ∧ ".join([f"¬{p}" for p in regla.get("excluidos", [])])
        
        if requeridos_str and excluidos_str:
            return f"({requeridos_str}) ∧ ({excluidos_str}) → {enfermedad}"
        elif requeridos_str:
            return f"({requeridos_str}) → {enfermedad}"
        elif excluidos_str:
            return f"({excluidos_str}) → {enfermedad}"
        else:
            return f"{enfermedad} (sin condiciones)"