"""
MÓDULO DE HERRAMIENTAS
Funciones comunes usadas en todo el sistema

UTILIDAD:
Este archivo centraliza todas las funciones auxiliares que son usadas por
múltiples módulos. Incluye funciones de interfaz (limpiar pantalla, pausar),
funciones de formato (líneas separadoras), y funciones de manejo de fechas
(validación, cálculo de días, indicadores de urgencia).

DEPENDENCIAS:
- os: Módulo estándar de Python para operaciones del sistema operativo,
  usado para limpiar la pantalla según el sistema (Windows/Linux/Mac)
- datetime: Módulo estándar de Python para trabajar con fechas,
  usado para validar formatos, calcular días restantes y comparar fechas

¿POR QUÉ NO DEPENDE DE OTROS ARCHIVOS DEL PROYECTO?
- herramientas.py es el módulo base que otros archivos usan
- No debe importar de otros módulos del proyecto para evitar dependencias circulares
- Solo usa módulos estándar de Python
"""

# Módulo estándar para operaciones del sistema operativo
import os
# Módulos estándar para trabajar con fechas y horas
from datetime import datetime, date

def limpiar_pantalla():
    """Limpia la pantalla del terminal"""
    # Ejecuta "cls" en Windows (nt) o "clear" en Linux/Mac
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pausa hasta que el usuario presione Enter"""
    # Espera que el usuario presione Enter antes de continuar
    input("\nPresione ENTER para continuar...")

def mostrar_despedida():
    """Muestra mensaje de despedida simple"""
    # Imprime un mensaje simple al salir del programa
    print("\nHasta luego!")

def linea_separadora(ancho=60, caracter="="):
    """Imprime una línea separadora

    Args:
        ancho: Número de caracteres de ancho (default 60)
        caracter: Caracter a usar para la línea (default "=")
    """
    # Repite el caracter las veces indicadas para formar una línea
    print(caracter * ancho)

def titulo_centrado(texto, ancho=60):
    """Imprime un título centrado"""
    # Usa el método center() para centrar el texto en el ancho especificado
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
        # Intenta convertir el string a fecha con el formato específico
        datetime.strptime(fecha_str, "%d/%m/%Y")
        # Si no hay error, la fecha es válida
        return True
    except ValueError:
        # Si hay error, el formato es incorrecto
        return False

def string_a_fecha(fecha_str):
    """Convierte string DD/MM/AAAA a objeto date"""
    try:
        # Convierte el string a datetime y extrae solo la fecha
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except:
        # Si hay cualquier error, retorna None
        return None

def calcular_dias_restantes(fecha_fin_str):
    """Calcula días restantes hasta la fecha de vencimiento

    Returns:
        int: días restantes (negativo si ya venció)
        None: si la fecha no es válida
    """
    # Primero convierte el string a objeto fecha
    fecha_fin = string_a_fecha(fecha_fin_str)
    # Si la conversión falló, retorna None
    if not fecha_fin:
        return None

    # Obtiene la fecha de hoy
    hoy = date.today()
    # Calcula la diferencia en días
    diferencia = (fecha_fin - hoy).days
    # Retorna el número de días (negativo si ya pasó)
    return diferencia

def obtener_indicador_urgencia(dias_restantes):
    """Devuelve un indicador textual según la urgencia

    Returns:
        str: indicador textual de urgencia
    """
    # Si no hay días calculados, retorna vacío
    if dias_restantes is None:
        return ""

    # Si la fecha ya pasó (días negativos)
    if dias_restantes < 0:
        # Convierte a positivo para mostrar cuántos días pasaron
        dias_vencido = abs(dias_restantes)
        # Maneja singular y plural correctamente
        if dias_vencido == 1:
            return "[VENCIDA 1 dia]"
        else:
            return f"[VENCIDA {dias_vencido} dias]"
    # Vence hoy
    elif dias_restantes == 0:
        return "[HOY]"
    # Vence mañana
    elif dias_restantes == 1:
        return "[MANANA]"
    # Urgente: vence en 2-3 días (usa corchetes)
    elif dias_restantes <= 3:
        return f"[{dias_restantes} dias]"
    # Moderado: vence en 4-7 días (usa paréntesis)
    elif dias_restantes <= 7:
        return f"({dias_restantes} dias)"
    # Con tiempo: más de 7 días (sin símbolos)
    else:
        return f"{dias_restantes} dias"

def formatear_fecha_corta(fecha_str):
    """Convierte DD/MM/AAAA a formato más corto DD/MM"""
    try:
        # Divide la fecha por las barras
        partes = fecha_str.split("/")
        # Si tiene las 3 partes (día, mes, año)
        if len(partes) == 3:
            # Retorna solo día y mes
            return f"{partes[0]}/{partes[1]}"
        # Si no tiene el formato esperado, retorna como está
        return fecha_str
    except:
        # Si hay cualquier error, retorna el string original
        return fecha_str