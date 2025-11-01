"""
MÓDULO DE UTILIDADES
Funciones comunes usadas en todo el sistema
"""

import os

def limpiar_pantalla():
    """Limpia la pantalla del terminal"""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pausa hasta que el usuario presione Enter"""
    input("\nPresione ENTER para continuar...")

def mostrar_despedida(estadisticas):
    """Muestra resumen final al salir

    Args:
        estadisticas: diccionario con total, completadas, pendientes, porcentaje_completado
    """
    print()
    linea_separadora(50)
    print("RESUMEN DE LA SESION")
    linea_separadora(50)
    print(f"Total de tareas: {estadisticas['total']}")
    print(f"Completadas: {estadisticas['completadas']}")
    print(f"Pendientes: {estadisticas['pendientes']}")
    if estadisticas['total'] > 0:
        print(f"Progreso: {estadisticas['porcentaje_completado']:.1f}%")
    print("\nHasta luego!")

def linea_separadora(ancho=60, caracter="="):
    """Imprime una línea separadora

    Args:
        ancho: Número de caracteres de ancho (default 60)
        caracter: Caracter a usar para la línea (default "=")
    """
    print(caracter * ancho)

def titulo_centrado(texto, ancho=60):
    """Imprime un título centrado"""
    print(texto.center(ancho))