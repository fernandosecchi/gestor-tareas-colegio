#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE GESTIÓN DE ARCHIVOS
================================================

Este módulo implementa la capa de persistencia del sistema.
Maneja la serialización/deserialización de datos en formato JSON.

Responsabilidades del módulo:
- Deserialización: cargar tareas desde archivo JSON
- Serialización: guardar tareas en JSON
- Validación y sanitización de datos durante la carga
- Manejo de errores de I/O (permisos, archivo inexistente)
- Creación de respaldos opcionales

Conceptos técnicos aplicados:
- Manejo de archivos con context managers (with)
- Codificación de caracteres (UTF-8)
- Manejo jerárquico de excepciones
- Validación de estructura de datos JSON
"""

# Importamos el módulo de tareas para acceder a sus funciones
import tareas
import json
import os

# ============================================
# CONSTANTES
# ============================================

# Archivo de persistencia en formato JSON (único)
NOMBRE_ARCHIVO_JSON = "tareas.json"


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def _normalizar_tarea_dict(info):
    """
    Normaliza una tarea desde JSON al esquema interno esperado.
    Garantiza presencia de claves y mapea fecha_entrega legacy a fecha_fin.
    """
    if not isinstance(info, dict):
        info = {}
    materia = info.get("materia", "")
    descripcion = info.get("descripcion", "")
    fecha_inicio = info.get("fecha_inicio", "")
    # Preferimos 'fecha_fin' explícita, luego 'fecha_entrega'
    _ff = info.get("fecha_fin", "")
    _fe = info.get("fecha_entrega", "")
    fecha_final = _ff or _fe or ""
    completada = bool(info.get("completada", False))
    codigo = info.get("codigo", "")
    observaciones = info.get("observaciones", "")
    return {
        "materia": materia,
        "descripcion": descripcion,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_final,
        "completada": completada,
        "codigo": codigo,
        "observaciones": observaciones,
    }

# ============================================
# FUNCIONES DE LECTURA
# ============================================

def cargar_tareas():
    """
    Carga las tareas exclusivamente desde JSON (tareas.json).
    Si no existe, inicializa el sistema sin tareas y crea el archivo
    al momento de guardar.
    
    Returns:
        bool: True si la carga fue exitosa, False si ocurrió un error
    """
    try:
        if os.path.exists(NOMBRE_ARCHIVO_JSON):
            with open(NOMBRE_ARCHIVO_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            origen = data.get("tareas") if isinstance(data, dict) else data
            tareas_cargadas = {}
            if isinstance(origen, dict):
                for k, info in origen.items():
                    try:
                        id_tarea = int(k)
                    except Exception:
                        id_tarea = int(info.get("id")) if isinstance(info, dict) and info.get("id") is not None else None
                    if id_tarea is None:
                        continue
                    tareas_cargadas[id_tarea] = _normalizar_tarea_dict(info)
            elif isinstance(origen, list):
                for elem in origen:
                    if not isinstance(elem, dict):
                        continue
                    if "id" not in elem:
                        continue
                    id_tarea = int(elem["id"])
                    info = {k: v for k, v in elem.items() if k != "id"}
                    tareas_cargadas[id_tarea] = _normalizar_tarea_dict(info)
            else:
                print("⚠️ Formato JSON no reconocido. No se cargaron tareas.")
                tareas_cargadas = {}
            tareas.establecer_tareas(tareas_cargadas)
            # Alinear los códigos con los IDs tras la carga
            try:
                tareas.sincronizar_codigos_con_ids()
            except Exception:
                pass
            return True
        
        # No existe JSON: inicializamos vacío
        tareas.establecer_tareas({})
        print("📝 Primera vez usando el programa. ¡Bienvenido!")
        print("   Se creará el archivo JSON al guardar las primeras tareas")
        return True
    except PermissionError:
        print("❌ Error: No hay permisos para leer el archivo de datos")
        return False
    except Exception as error:
        print(f"❌ Error inesperado al cargar tareas: {error}")
        return False


# ============================================
# FUNCIONES DE ESCRITURA
# ============================================

def guardar_tareas():
    """
    Persiste todas las tareas exclusivamente en JSON (tareas.json).
    
    Returns:
        bool: True si el guardado fue exitoso, False si ocurrió un error
    """
    try:
        tareas_actuales = tareas.obtener_tareas()
        cantidad = len(tareas_actuales)

        # Preparar estructura normalizada para persistencia
        tareas_para_guardar = {}
        for id_tarea, info in sorted(tareas_actuales.items()):
            materia = info.get("materia", "")
            descripcion = info.get("descripcion", "")
            fecha_inicio = info.get("fecha_inicio", "")
            fecha_fin = info.get("fecha_fin", "")
            completada_bool = bool(info.get("completada", False))
            codigo = info.get("codigo", "")
            observaciones = info.get("observaciones", "")

            tareas_para_guardar[str(id_tarea)] = {
                "materia": materia,
                "descripcion": descripcion,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "completada": completada_bool,
                "codigo": codigo,
                "observaciones": observaciones,
            }

        # Guardado en JSON
        try:
            payload = {"version": 1, "tareas": tareas_para_guardar}
            with open(NOMBRE_ARCHIVO_JSON, "w", encoding="utf-8") as jf:
                json.dump(payload, jf, ensure_ascii=False, indent=2)
            if cantidad > 0:
                print(f"💾 Se guardaron {cantidad} tarea{'s' if cantidad != 1 else ''} (JSON)")
            return True
        except Exception as e:
            print(f"⚠️ No se pudo escribir JSON: {e}")
            return False

    except PermissionError:
        print("❌ Error: No hay permisos para escribir el archivo de datos")
        return False
    except Exception as error:
        print(f"❌ Error al guardar tareas: {error}")
        return False


# ============================================
# FUNCIONES DE RESPALDO
# ============================================

def crear_respaldo():
    """
    Crea un archivo de respaldo de las tareas (solo JSON).
    
    Returns:
        bool: True si se creó el respaldo, False si hubo error
    """
    try:
        import shutil
        from datetime import datetime
        
        if not os.path.exists(NOMBRE_ARCHIVO_JSON):
            print("⚠️ No hay archivo para respaldar")
            return False
        
        origen = NOMBRE_ARCHIVO_JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_respaldo = f"tareas_respaldo_{timestamp}.json"
        
        shutil.copy2(origen, nombre_respaldo)
        print(f"📋 Respaldo creado: {nombre_respaldo}")
        return True
        
    except FileNotFoundError:
        print("⚠️ No hay archivo para respaldar")
        return False
        
    except Exception as error:
        print(f"❌ Error al crear respaldo: {error}")
        return False


def existe_archivo():
    """
    Verifica si existe el archivo de tareas JSON.
    
    Returns:
        bool: True si existe, False si no
    """
    return os.path.exists(NOMBRE_ARCHIVO_JSON)


def obtener_info_archivo():
    """
    Obtiene información sobre el archivo de tareas JSON.
    
    Returns:
        dict: Diccionario con información del archivo o None si no existe
    """
    from datetime import datetime
    
    try:
        if not os.path.exists(NOMBRE_ARCHIVO_JSON):
            return None
        ruta = NOMBRE_ARCHIVO_JSON
        stat = os.stat(ruta)
        info = {
            "archivo": ruta,
            "tamaño": stat.st_size,
            "tamaño_legible": f"{stat.st_size / 1024:.2f} KB" if stat.st_size > 1024 else f"{stat.st_size} bytes",
            "modificado": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                info["lineas"] = sum(1 for _ in f)
        except Exception:
            info["lineas"] = None
        return info
    except FileNotFoundError:
        return None
    except Exception:
        return None
