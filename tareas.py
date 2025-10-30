#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE GESTIÓN DE TAREAS
================================================

Este módulo implementa la lógica de negocio para la gestión de tareas.

Responsabilidades del módulo:
- Creación y eliminación de tareas
- Consulta y filtrado de tareas
- Modificación de estados (marcar como completada)
- Cálculo de estadísticas agregadas
- Gestión del almacenamiento en memoria (diccionario)

Conceptos técnicos aplicados:
- Diccionarios como estructura de datos principal
- Variables globales y modificadores (global)
- Generación de IDs autoincrementales
- Funciones puras vs funciones con efectos secundarios
- Filtrado y agregación de datos
"""

# ============================================
# VARIABLES GLOBALES DEL MÓDULO
# ============================================

# Diccionario principal que almacena todas las tareas del sistema
# Estructura de datos: cada tarea se identifica por un ID único (número entero)
# Formato: {id: {"materia": str, "descripcion": str, "fecha_fin": str, "completada": bool}}
# Ejemplo práctico: {1: {"materia": "Matemáticas", "descripcion": "Ejercicios", ...}}
tareas_colegio = {}

# Contador autoincremental para generar IDs únicos
# Funciona como un ticket en un banco: cada nueva tarea recibe el siguiente número
# Se incrementa automáticamente después de crear cada tarea
siguiente_id = 1


# ============================================
# FUNCIONES PARA GESTIONAR TAREAS
# ============================================

def obtener_tareas():
    """
    Retorna el diccionario completo de tareas.
    
    Esta función proporciona acceso de solo lectura a todas las tareas almacenadas.
    Es útil cuando otros módulos necesitan consultar o iterar sobre las tareas.
    
    Returns:
        dict: Diccionario con todas las tareas del sistema
    """
    return tareas_colegio


def sincronizar_codigos_con_ids():
    """
    Asegura que el campo 'codigo' de cada tarea esté alineado con su ID.
    Genera y asigna el código con el formato T-XXXX para cada ID existente.
    """
    for id_tarea, info in tareas_colegio.items():
        try:
            info["codigo"] = generar_codigo_tarea(id_tarea)
        except Exception:
            # Si por algún motivo falla, mantenemos el valor anterior
            pass


def obtener_siguiente_id():
    """
    Devuelve el siguiente ID disponible.
    
    Returns:
        int: Siguiente ID a usar
    """
    return siguiente_id


def generar_codigo_tarea(id_tarea):
    """
    Genera un código de tarea a partir del ID.
    El formato es "T-XXXX" donde XXXX es el ID con cero padding a 4 dígitos.
    """
    try:
        return f"T-{int(id_tarea):04d}"
    except Exception:
        # Fallback en caso de que no pueda convertirse a int
        return f"T-{id_tarea}"


def establecer_tareas(nuevas_tareas):
    """
    Reemplaza el conjunto actual de tareas con uno nuevo.
    
    Esta función se utiliza principalmente durante la carga de datos desde archivo.
    Actualiza tanto el diccionario de tareas como el contador de IDs.
    
    Args:
        nuevas_tareas (dict): Diccionario con las tareas a establecer
    """
    global tareas_colegio, siguiente_id
    tareas_colegio = nuevas_tareas
    
    # Recalculamos el siguiente ID basándonos en el ID más alto existente
    # Esto asegura que no haya colisiones al crear nuevas tareas
    # Ejemplo: si los IDs existentes son [1, 2, 5], el siguiente será 6
    if tareas_colegio:
        siguiente_id = max(tareas_colegio.keys()) + 1
    else:
        siguiente_id = 1  # Iniciamos desde 1 si no hay tareas


def agregar_tarea(materia, descripcion, fecha_fin, fecha_inicio="", completada=False, codigo="", observaciones=""):
    """
    Crea una nueva tarea en el sistema.
    
    Esta función es responsable de:
    1. Asignar un ID único a la nueva tarea
    2. Crear un diccionario con todos los datos de la tarea
    3. Almacenarla en el diccionario principal
    4. Incrementar el contador de IDs
    
    Args:
        materia (str): Nombre de la asignatura (ej: "Matemáticas")
        descripcion (str): Detalle de lo que hay que hacer (ej: "Ejercicios 1 al 10")
        fecha_fin (str): Fecha de vencimiento en formato libre (ej: "Mañana", "15/03")
        fecha_inicio (str): Fecha de inicio (opcional)
        completada (bool): Estado de la tarea (False=en proceso, True=completada)
        codigo (str): (Ignorado) El código de la tarea ahora se genera automáticamente a partir del ID.
        observaciones (str): Observaciones o notas (opcional)
        
    Returns:
        int: ID asignado a la tarea recién creada
    """
    global siguiente_id
    
    # Generamos el código en función del ID que se va a asignar
    codigo_generado = generar_codigo_tarea(siguiente_id)

    # Creamos un nuevo registro con todos los campos de la tarea
    tareas_colegio[siguiente_id] = {
        "materia": materia,
        "descripcion": descripcion,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "completada": bool(completada),
        "codigo": codigo_generado,
        "observaciones": observaciones,
    }
    
    # Guardamos el ID actual antes de incrementarlo
    id_creado = siguiente_id
    
    # Incrementamos el contador para que la próxima tarea tenga un ID diferente
    siguiente_id += 1
    
    return id_creado


def obtener_tarea(id_tarea):
    """
    Obtiene una tarea específica por su ID.
    
    Args:
        id_tarea (int): ID de la tarea
        
    Returns:
        dict: Información de la tarea o None si no existe
    """
    return tareas_colegio.get(id_tarea)


def marcar_completada(id_tarea):
    """
    Marca una tarea como completada.
    
    Modifica el campo 'completada' de False a True para la tarea especificada.
    Esta operación es irreversible en la versión actual del programa.
    
    Args:
        id_tarea (int): Identificador de la tarea a marcar
        
    Returns:
        bool: True si la operación fue exitosa, False si el ID no existe
    """
    # Verificamos la existencia de la tarea antes de modificarla
    if id_tarea in tareas_colegio:
        # Actualizamos el estado de la tarea
        tareas_colegio[id_tarea]["completada"] = True
        return True
    return False  # El ID no corresponde a ninguna tarea


def eliminar_tarea(id_tarea):
    """
    Elimina una tarea del sistema.
    
    Args:
        id_tarea (int): ID de la tarea a eliminar
        
    Returns:
        bool: True si se eliminó, False si no existe
    """
    if id_tarea in tareas_colegio:
        del tareas_colegio[id_tarea]
        return True
    return False


def obtener_tareas_pendientes():
    """
    Filtra y retorna únicamente las tareas pendientes.
    
    Itera sobre todas las tareas y selecciona aquellas cuyo campo 'completada' es False.
    Útil para mostrar al usuario qué trabajo le queda por hacer.
    
    Returns:
        dict: Nuevo diccionario conteniendo solo las tareas no completadas
    """
    pendientes = {}  # Diccionario temporal para almacenar resultados
    
    # Iteramos sobre cada entrada del diccionario principal
    for id_tarea, info in tareas_colegio.items():
        # Verificamos el estado de completitud
        if not info["completada"]:
            pendientes[id_tarea] = info
    
    return pendientes


def obtener_tareas_completadas():
    """
    Obtiene todas las tareas que están completadas.
    
    Returns:
        dict: Diccionario con solo las tareas completadas
    """
    completadas = {}
    for id_tarea, info in tareas_colegio.items():
        if info["completada"]:
            completadas[id_tarea] = info
    return completadas


def obtener_tareas_por_materia(nombre_materia):
    """
    Obtiene todas las tareas de una materia específica.
    
    Args:
        nombre_materia (str): Nombre de la materia a buscar
        
    Returns:
        dict: Diccionario con las tareas de esa materia
    """
    tareas_materia = {}
    for id_tarea, info in tareas_colegio.items():
        if info["materia"].lower() == nombre_materia.lower():
            tareas_materia[id_tarea] = info
    return tareas_materia


def obtener_estadisticas():
    """
    Calcula y retorna estadísticas agregadas sobre las tareas.
    
    Esta función realiza varios cálculos:
    - Conteo total de tareas
    - Conteo de tareas completadas y pendientes
    - Porcentaje de progreso
    - Estadísticas desglosadas por materia
    
    Returns:
        dict: Diccionario con claves 'total', 'completadas', 'pendientes', 
              'porcentaje' y 'por_materia'
    """
    # Calculamos la cantidad total de tareas usando len()
    total = len(tareas_colegio)
    
    # Contamos tareas completadas usando una expresión generadora
    # sum() suma 1 por cada tarea donde completada == True
    completadas = sum(1 for t in tareas_colegio.values() if t["completada"])
    
    # Las pendientes se obtienen por diferencia
    pendientes = total - completadas
    
    # Generamos estadísticas agrupadas por materia
    # Este diccionario tendrá una entrada por cada materia única
    por_materia = {}
    for info in tareas_colegio.values():
        materia = info["materia"]
        
        # Inicializamos el registro si es la primera tarea de esta materia
        if materia not in por_materia:
            por_materia[materia] = {"total": 0, "completadas": 0, "pendientes": 0}
        
        # Incrementamos los contadores correspondientes
        por_materia[materia]["total"] += 1
        
        if info["completada"]:
            por_materia[materia]["completadas"] += 1
        else:
            por_materia[materia]["pendientes"] += 1
    
    # Calculamos el porcentaje de progreso
    # Fórmula: (completadas / total) * 100
    # Ejemplo: 5 de 10 tareas = (5/10)*100 = 50%
    porcentaje = 0
    if total > 0:  # Evitamos división por cero
        porcentaje = (completadas / total) * 100
    
    # Retornamos todas las estadísticas en un diccionario estructurado
    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "porcentaje": porcentaje,
        "por_materia": por_materia
    }


def contar_tareas():
    """
    Cuenta el total de tareas.
    
    Returns:
        int: Número total de tareas
    """
    return len(tareas_colegio)


def hay_tareas():
    """
    Verifica si hay tareas registradas.
    
    Returns:
        bool: True si hay tareas, False si no
    """
    return len(tareas_colegio) > 0
