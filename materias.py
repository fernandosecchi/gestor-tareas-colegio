#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE GESTIÓN DE MATERIAS
================================================

Este módulo maneja todo lo relacionado con las
materias escolares disponibles.

Responsabilidades:
- Mantener la lista de materias disponibles
- Permitir la selección de materias
- Validar materias personalizadas

Conceptos que aprenderás:
- Listas y su manipulación
- Constantes en Python
- Funciones de validación
- Enumeración de elementos
"""

# ============================================
# CONSTANTES DEL MÓDULO
# ============================================

# Lista de materias predefinidas
# Usamos una tupla porque no debe modificarse
MATERIAS_PREDEFINIDAS = (
    "Matemáticas",
    "Lengua",
    "Historia",
    "Geografía",
    "Ciencias Naturales",
    "Inglés",
    "Educación Física",
    "Arte",
    "Música",
    "Informática",
    "Física",
    "Química",
    "Biología",
    "Otra"  # Permite al usuario ingresar una materia personalizada
)


# Códigos de materias (código -> nombre)
# Mantiene compatibilidad: las tareas siguen guardando solo el nombre de la materia.
MATERIAS_CON_CODIGO = [
    ("MAT", "Matemáticas"),
    ("LEN", "Lengua"),
    ("HIS", "Historia"),
    ("GEO", "Geografía"),
    ("CN",  "Ciencias Naturales"),
    ("ING", "Inglés"),
    ("EF",  "Educación Física"),
    ("ART", "Arte"),
    ("MUS", "Música"),
    ("INF", "Informática"),
    ("FIS", "Física"),
    ("QUI", "Química"),
    ("BIO", "Biología"),
    ("OTR", "Otra"),
]

# Mapas auxiliares para búsquedas rápidas
CODIGO_A_NOMBRE = {cod: nom for cod, nom in MATERIAS_CON_CODIGO}
NOMBRE_A_CODIGO = {nom: cod for cod, nom in MATERIAS_CON_CODIGO}


def obtener_materias_con_codigo():
    """
    Devuelve un diccionario {codigo: nombre} de materias disponibles.
    No modificar directamente desde afuera.
    """
    return dict(CODIGO_A_NOMBRE)


def obtener_nombre_por_codigo(codigo):
    """Devuelve el nombre de la materia para un código dado (case-insensitive)."""
    if not codigo:
        return None
    return CODIGO_A_NOMBRE.get(codigo.strip().upper())


def obtener_codigo_por_nombre(nombre):
    """Devuelve el código de una materia por su nombre exacto, o None si no existe."""
    return NOMBRE_A_CODIGO.get(nombre)


# ============================================
# FUNCIONES DEL MÓDULO
# ============================================

def obtener_materias():
    """
    Devuelve la lista de materias disponibles.
    
    Returns:
        tuple: Tupla con las materias predefinidas
    """
    return MATERIAS_PREDEFINIDAS


def mostrar_materias():
    """
    Muestra las materias disponibles en formato numerado y con código.
    No retorna nada, solo imprime en pantalla.
    """
    print("\n📚 MATERIAS DISPONIBLES:")
    print("-" * 30)
    
    # enumerate() agrega números a cada elemento
    # Empezamos desde 1 para que sea más amigable al usuario
    for indice, (codigo, nombre) in enumerate(MATERIAS_CON_CODIGO, 1):
        # :2 alinea los números a 2 espacios
        print(f"{indice:2}. {codigo} - {nombre}")


def validar_seleccion(numero):
    """
    Valida si el número seleccionado es válido.
    
    Args:
        numero (int): Número seleccionado por el usuario

        
    Returns:
        bool: True si es válido, False si no
    """
    return 1 <= numero <= len(MATERIAS_CON_CODIGO)


def obtener_materia_por_indice(indice):
    """
    Obtiene una materia por su índice (basado en 1).
    
    Args:
        indice (int): Índice de la materia (1 a N)
        
    Returns:
        str: Nombre de la materia o None si el índice es inválido
    """
    if validar_seleccion(indice):
        # Restamos 1 porque las listas empiezan en 0
        return MATERIAS_CON_CODIGO[indice - 1][1]
    return None


def es_materia_personalizada(materia):
    """
    Verifica si la materia seleccionada es "Otra".
    
    Args:
        materia (str): Nombre de la materia
        
    Returns:
        bool: True si es "Otra", False si no
    """
    return materia == "Otra"


def validar_nombre_materia(nombre):
    """
    Valida que el nombre de una materia sea válido.
    
    Args:
        nombre (str): Nombre a validar
        
    Returns:
        bool: True si es válido, False si no
    """
    # El nombre debe tener al menos 2 caracteres y no ser solo espacios
    return nombre and len(nombre.strip()) >= 2


def seleccionar_materia():
    """
    Permite al usuario seleccionar una materia de forma interactiva.
    Acepta tanto número (1..N) como código (p. ej., MAT, ING, OTR).
    Devuelve SIEMPRE el nombre de la materia. Si elige "OTR/Otra",
    solicita un nombre personalizado.
    """
    # Mostramos las opciones
    mostrar_materias()
    
    # Bucle hasta obtener una selección válida
    while True:
        try:
            entrada = input("\n📝 Seleccione el número o código de la materia: ").strip()

            # Si ingresa vacío, pedir nuevamente
            if not entrada:
                print("❌ Debe ingresar un número o un código de materia")
                continue

            # 1) Si ingresó un número
            if entrada.isdigit():
                opcion = int(entrada)
                if validar_seleccion(opcion):
                    materia = obtener_materia_por_indice(opcion)
                    if es_materia_personalizada(materia):
                        while True:
                            nombre_personalizado = input("📝 Escriba el nombre de la materia: ").strip()
                            if validar_nombre_materia(nombre_personalizado):
                                return nombre_personalizado
                            else:
                                print("❌ El nombre debe tener al menos 2 caracteres")
                    else:
                        return materia
                else:
                    print(f"❌ Opción no válida. Elija un número del 1 al {len(MATERIAS_CON_CODIGO)}")
                    continue

            # 2) Si ingresó un código
            nombre = obtener_nombre_por_codigo(entrada)
            if nombre:
                if es_materia_personalizada(nombre):
                    while True:
                        nombre_personalizado = input("📝 Escriba el nombre de la materia: ").strip()
                        if validar_nombre_materia(nombre_personalizado):
                            return nombre_personalizado
                        else:
                            print("❌ El nombre debe tener al menos 2 caracteres")
                else:
                    return nombre

            # Si llegó aquí, ni número válido ni código reconocido
            print("❌ Entrada no válida. Ingrese un número o un código existente (por ej., MAT, ING, OTR).")

        except KeyboardInterrupt:
            print("\n❌ Selección cancelada")
            raise


def buscar_materia_similar(nombre_buscar):
    """
    Busca materias similares al nombre dado.
    Útil para búsquedas flexibles.
    
    Args:
        nombre_buscar (str): Nombre a buscar
        
    Returns:
        list: Lista de materias que coinciden parcialmente
    """
    coincidencias = []
    nombre_buscar = nombre_buscar.lower()
    
    for materia in MATERIAS_PREDEFINIDAS:
        if materia != "Otra":  # Excluimos "Otra" de las búsquedas
            if nombre_buscar in materia.lower():
                coincidencias.append(materia)
    
    return coincidencias
