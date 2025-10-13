#!/usr/bin/env python3


import tkinter as tk
from Interfaz import Interfaz

def main():
    # Inicia la aplicación de interfaz gráfica
    try:
        root = tk.Tk()
        app = Interfaz(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()