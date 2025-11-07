import logging
import sys
import traceback
import ttkbootstrap as ttk
from tkinter import messagebox
import pathlib
try:
    from logica import LogicaProposicional
    from interfaz import InterfazEntrevistaGrafica
except ImportError:
    print("ERROR: Asegúrate de tener los archivos 'logica.py' y 'interfaz.py' en la misma carpeta.")
    sys.exit(1)


# --- Configuración de Logging ---
logging.basicConfig(
    level=logging.WARNING, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sistema_experto.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LanzadorEntrevista")

def main():
    try:
        script_dir = pathlib.Path(__file__).parent.resolve()
        RUTA_BASE_CONOCIMIENTO = script_dir / "base_de_conocimiento.json"

        logger.info("Iniciando el Sistema Experto (Modo Entrevista GUI)...")
        
        sistema_experto = LogicaProposicional(RUTA_BASE_CONOCIMIENTO)
        
        ventana_raiz = ttk.Window(themename="flatly") 
        
        app = InterfazEntrevistaGrafica(ventana_raiz, sistema_experto)
        
        ventana_raiz.mainloop()
        
    except FileNotFoundError:
        logger.critical(f"Error: No se encontró el archivo '{RUTA_BASE_CONOCIMIENTO}'.")
        messagebox.showerror("Error Fatal", f"No se pudo encontrar el archivo de reglas: {RUTA_BASE_CONOCIMIENTO}")
    except Exception as e:
        logger.critical(f"Error fatal en la aplicación: {e}")
        logger.critical(traceback.format_exc())
        messagebox.showerror("Error Fatal", f"Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    main()