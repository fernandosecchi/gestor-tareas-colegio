#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        GESTOR DE TAREAS DEL COLEGIO
        Archivo principal (punto de entrada)
================================================

Este módulo actúa como punto de entrada de la aplicación.
Responsabilidad única: iniciar y coordinar el flujo principal del programa.

Conceptos implementados:
- Importación de módulos personalizados
- Patrón main() como función de entrada
- Guard clause con if __name__ == "__main__"
- Manejo robusto de excepciones (KeyboardInterrupt, Exception)
"""

# Importamos los módulos que necesitamos
from menu import ejecutar_menu_principal
from archivo import cargar_tareas, guardar_tareas
from utils import mostrar_bienvenida, mostrar_despedida


def main():
    """
    Función principal del programa - punto de entrada de la ejecución.
    
    Coordina el flujo general de la aplicación en el siguiente orden:
    1. Muestra mensaje de bienvenida
    2. Carga datos persistentes desde el archivo
    3. Inicia el bucle del menú interactivo
    4. Guarda el estado actual antes de terminar
    5. Muestra mensaje de despedida
    
    También maneja excepciones para garantizar el guardado de datos en caso de errores.
    """
    try:
        # Mostramos mensaje inicial al usuario
        mostrar_bienvenida()
        
        # Cargamos las tareas desde el archivo de persistencia
        cargar_tareas()
        
        # Iniciamos el bucle principal del menú
        # Esta función bloquea hasta que el usuario elija salir
        ejecutar_menu_principal()
        
        # Persistimos el estado actual antes de terminar
        guardar_tareas()
        
        # Mostramos mensaje de despedida
        mostrar_despedida()
        
    except KeyboardInterrupt:
        # Manejo de interrupción manual (Ctrl+C)
        # Aseguramos que los datos se guarden incluso en salida abrupta
        print("\n\n⚠️ Programa interrumpido por el usuario")
        print("💾 Guardando tareas antes de salir...")
        guardar_tareas()
        print("¡Hasta luego! 👋")
        
    except Exception as error:
        # Captura de excepciones genéricas - última línea de defensa
        # Intentamos guardar los datos incluso si hay un error crítico
        print(f"\n❌ Error inesperado: {error}")
        print("💾 Intentando guardar las tareas...")
        try:
            guardar_tareas()
        except:
            print("No se pudieron guardar las tareas")


# ============================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================
if __name__ == "__main__":
    # Guard para ejecución directa del script
    # Esta condición es True solo cuando el archivo se ejecuta directamente,
    # no cuando se importa como módulo en otro archivo.
    # Permite que el código sea reutilizable y testeable.
    main()
