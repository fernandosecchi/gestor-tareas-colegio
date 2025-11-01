"""
MÓDULO DE UTILIDADES
Funciones comunes usadas en todo el sistema
"""

import os
from datetime import datetime, date

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

# ============================================
# FUNCIONES DE FECHA
# ============================================

def validar_fecha(fecha_str):
    """Valida que una fecha tenga el formato DD/MM/AAAA

    Returns:
        True si la fecha es válida, False en caso contrario
    """
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def string_a_fecha(fecha_str):
    """Convierte string DD/MM/AAAA a objeto date"""
    try:
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except:
        return None

def calcular_dias_restantes(fecha_fin_str):
    """Calcula días restantes hasta la fecha de vencimiento

    Returns:
        int: días restantes (negativo si ya venció)
        None: si la fecha no es válida
    """
    fecha_fin = string_a_fecha(fecha_fin_str)
    if not fecha_fin:
        return None

    hoy = date.today()
    diferencia = (fecha_fin - hoy).days
    return diferencia

def obtener_indicador_urgencia(dias_restantes):
    """Devuelve un indicador textual según la urgencia

    Returns:
        str: indicador textual de urgencia
    """
    if dias_restantes is None:
        return ""

    if dias_restantes < 0:
        dias_vencido = abs(dias_restantes)
        if dias_vencido == 1:
            return "[VENCIDA 1 dia]"
        else:
            return f"[VENCIDA {dias_vencido} dias]"
    elif dias_restantes == 0:
        return "[HOY]"
    elif dias_restantes == 1:
        return "[MANANA]"
    elif dias_restantes <= 3:
        return f"[{dias_restantes} dias]"
    elif dias_restantes <= 7:
        return f"({dias_restantes} dias)"
    else:
        return f"{dias_restantes} dias"

def formatear_fecha_corta(fecha_str):
    """Convierte DD/MM/AAAA a formato más corto DD/MM"""
    try:
        partes = fecha_str.split("/")
        if len(partes) == 3:
            return f"{partes[0]}/{partes[1]}"
        return fecha_str
    except:
        return fecha_str