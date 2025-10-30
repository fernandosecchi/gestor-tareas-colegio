#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE UTILIDADES
================================================

Este módulo contiene funciones de utilidad general
que son usadas por otros módulos.

Responsabilidades:
- Funciones de formateo
- Mensajes del sistema
- Utilidades de interfaz
- Funciones auxiliares

Conceptos que aprenderás:
- Funciones reutilizables
- Modularización del código
- Separación de responsabilidades
"""

import tareas
import os
import sys


# ============================================
# FUNCIONES DE INTERFAZ
# ============================================

def limpiar_pantalla():
    """
    Limpia la pantalla según el sistema operativo.
    """
    # Detectamos el sistema operativo
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def pausar():
    """
    Hace una pausa hasta que el usuario presione Enter.
    Útil para dar tiempo a leer los mensajes.
    """
    input("\n➡️ Presione Enter para volver al menú...")


def linea_separadora(caracter="=", longitud=60):
    """
    Crea una línea separadora.
    
    Args:
        caracter (str): Carácter a usar para la línea
        longitud (int): Longitud de la línea
        
    Returns:
        str: Línea separadora
    """
    return caracter * longitud


# ============================================
# FUNCIONES DE MENSAJES
# ============================================

def mostrar_bienvenida():
    """
    Muestra el mensaje de bienvenida al iniciar el programa.
    """
    pass


def mostrar_despedida():
    """
    Muestra el mensaje de despedida al salir del programa.
    """
    print("\n" + "=" * 60)
    print("         👋 ¡HASTA LUEGO!")
    print("=" * 60)
    
    # Obtenemos estadísticas para el mensaje final
    stats = tareas.obtener_estadisticas()
    
    if stats['total'] > 0:
        if stats['pendientes'] > 0:
            print(f"⏰ Recuerda: tienes {stats['pendientes']} tarea{'s' if stats['pendientes'] != 1 else ''} pendiente{'s' if stats['pendientes'] != 1 else ''}")
            
            # Mensaje motivacional según la cantidad
            if stats['pendientes'] <= 3:
                print("   ¡Casi terminas! Un último esfuerzo 💪")
            elif stats['pendientes'] <= 7:
                print("   ¡Tú puedes! Organiza tu tiempo y lo lograrás 📚")
            else:
                print("   Divide y conquista. Una tarea a la vez 🎯")
        else:
            print("🎉 ¡Todas las tareas completadas! ¡Excelente trabajo!")
            print("   Disfruta tu tiempo libre, te lo has ganado 🌟")
    else:
        print("📝 No olvides agregar tus tareas la próxima vez")
    
    print("\n¡Que tengas un excelente día! 📚✨")
    print("=" * 60)


def mostrar_error(mensaje):
    """
    Muestra un mensaje de error formateado.
    
    Args:
        mensaje (str): Mensaje de error a mostrar
    """
    print(f"\n❌ ERROR: {mensaje}")


def mostrar_exito(mensaje):
    """
    Muestra un mensaje de éxito formateado.
    
    Args:
        mensaje (str): Mensaje de éxito a mostrar
    """
    print(f"\n✅ ÉXITO: {mensaje}")


def mostrar_advertencia(mensaje):
    """
    Muestra un mensaje de advertencia formateado.
    
    Args:
        mensaje (str): Mensaje de advertencia a mostrar
    """
    print(f"\n⚠️ ADVERTENCIA: {mensaje}")


# ============================================
# FUNCIONES DE FORMATEO
# ============================================

def truncar_texto(texto, longitud_maxima):
    """
    Trunca un texto si excede la longitud máxima.
    
    Args:
        texto (str): Texto a truncar
        longitud_maxima (int): Longitud máxima permitida
        
    Returns:
        str: Texto truncado con "..." si fue necesario
    """
    if len(texto) > longitud_maxima:
        return texto[:longitud_maxima] + "..."
    return texto


def formatear_fecha(fecha):
    """
    Formatea una fecha para mostrarla de forma más amigable.
    
    Por ahora solo devuelve la fecha tal cual, pero podríamos
    expandir esto para dar formato especial.
    
    Args:
        fecha (str): Fecha a formatear
        
    Returns:
        str: Fecha formateada
    """
    # Por ahora devolvemos la fecha tal cual
    # En el futuro podríamos agregar formato especial
    return fecha


def centrar_texto(texto, ancho=60):
    """
    Centra un texto en un ancho específico.
    
    Args:
        texto (str): Texto a centrar
        ancho (int): Ancho total de la línea
        
    Returns:
        str: Texto centrado
    """
    return texto.center(ancho)


def crear_titulo(texto, simbolo="=", ancho=60):
    """
    Crea un título formateado con líneas decorativas.
    
    Args:
        texto (str): Texto del título
        simbolo (str): Símbolo para las líneas
        ancho (int): Ancho total
        
    Returns:
        str: Título formateado
    """
    linea = simbolo * ancho
    titulo_centrado = centrar_texto(texto, ancho)
    
    return f"{linea}\n{titulo_centrado}\n{linea}"


# ============================================
# FUNCIONES DE VALIDACIÓN
# ============================================

def es_entero_valido(texto):
    """
    Verifica si un texto puede convertirse a entero.
    
    Args:
        texto (str): Texto a verificar
        
    Returns:
        bool: True si es un entero válido, False si no
    """
    try:
        int(texto)
        return True
    except ValueError:
        return False


def validar_texto_no_vacio(texto):
    """
    Valida que un texto no esté vacío o solo con espacios.
    
    Args:
        texto (str): Texto a validar
        
    Returns:
        bool: True si el texto es válido, False si no
    """
    return texto and texto.strip() != ""


def confirmar_accion(mensaje="¿Está seguro?"):
    """
    Pide confirmación al usuario para una acción.
    
    Args:
        mensaje (str): Mensaje de confirmación
        
    Returns:
        bool: True si confirma, False si no
    """
    respuesta = input(f"\n{mensaje} (S/N): ").upper().strip()
    return respuesta == "S"


# ============================================
# FUNCIONES DE INFORMACIÓN
# ============================================

def obtener_version():
    """
    Devuelve la versión del programa.
    
    Returns:
        str: Versión del programa
    """
    return "1.0.0"


def obtener_autor():
    """
    Devuelve el autor del programa.
    
    Returns:
        str: Autor del programa
    """
    return "Estudiante de Python"


def mostrar_ayuda():
    """
    Muestra la ayuda del programa.
    """
    print("\n" + "=" * 60)
    print("         📖 AYUDA DEL PROGRAMA")
    print("=" * 60)
    
    print("\nOPCIONES DISPONIBLES:")
    print("-" * 40)
    print("1. Agregar tarea: Permite crear una nueva tarea")
    print("2. Ver todas: Muestra todas las tareas organizadas")
    print("3. Por materia: Filtra las tareas de una materia")
    print("4. Completar: Marca una tarea como terminada")
    print("5. Eliminar: Borra una tarea del sistema")
    print("6. Pendientes: Muestra solo lo que falta hacer")
    print("7. Estadísticas: Muestra análisis detallado")
    print("8. Salir: Guarda y cierra el programa")
    
    print("\nCONSEJOS:")
    print("-" * 40)
    print("• Usa fechas descriptivas (Lunes, Mañana, etc.)")
    print("• Las tareas se guardan automáticamente")
    print("• Puedes usar Ctrl+C para salir en emergencia")
    print("• El archivo de tareas es 'tareas.json'")
    
    print("\nVERSIÓN:", obtener_version())
    print("AUTOR:", obtener_autor())
    print("=" * 60)
