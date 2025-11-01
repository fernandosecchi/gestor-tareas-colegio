"""
GESTOR DE TAREAS DEL COLEGIO
"""

from materias import seleccionar_materia
from utils import (
    limpiar_pantalla, pausar, linea_separadora,
    validar_fecha, calcular_dias_restantes,
    obtener_indicador_urgencia, formatear_fecha_corta,
    string_a_fecha
)

# ============================================
# DATOS GLOBALES (en memoria)
# ============================================
tareas_colegio = {}  # {codigo: {materia, descripcion, fecha_fin, completada}}
siguiente_numero = 1

# ============================================
# FUNCIONES DE GESTIÓN DE TAREAS
# ============================================

def obtener_tareas():
    """Devuelve todas las tareas"""
    return tareas_colegio

def generar_codigo():
    """Genera un código único con formato T001, T002, etc."""
    global siguiente_numero
    codigo = f"T{siguiente_numero:03d}"
    siguiente_numero += 1
    return codigo

def agregar_tarea(materia, tarea, fecha_inicio, fecha_fin, observaciones=""):
    """Agrega una nueva tarea con todos los campos requeridos"""
    codigo = generar_codigo()

    tareas_colegio[codigo] = {
        "materia": materia,
        "tarea": tarea,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "estado": "En proceso",  # "En proceso" o "Completada"
        "codigo": codigo,
        "observaciones": observaciones
    }

    return codigo

def obtener_tarea(codigo):
    """Obtiene una tarea por su código"""
    return tareas_colegio.get(codigo, None)

def marcar_completada(codigo):
    """Marca una tarea como completada"""
    if codigo in tareas_colegio:
        tareas_colegio[codigo]["estado"] = "Completada"
        return True
    return False

def eliminar_tarea(codigo):
    """Elimina una tarea"""
    if codigo in tareas_colegio:
        del tareas_colegio[codigo]
        return True
    return False

def obtener_tareas_pendientes():
    """Devuelve solo las tareas en proceso"""
    return {cod: info for cod, info in tareas_colegio.items()
            if info.get("estado") == "En proceso"}

def obtener_tareas_completadas():
    """Devuelve solo las tareas completadas"""
    return {cod: info for cod, info in tareas_colegio.items()
            if info.get("estado") == "Completada"}

def obtener_estadisticas():
    """Calcula estadísticas de las tareas"""
    total = len(tareas_colegio)
    completadas = sum(1 for t in tareas_colegio.values() if t.get("estado") == "Completada")
    pendientes = total - completadas

    porcentaje = 0
    if total > 0:
        porcentaje = (completadas / total) * 100

    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "porcentaje_completado": porcentaje
    }

def obtener_tareas_ordenadas_por_fecha():
    """Devuelve las tareas ordenadas por fecha de vencimiento (más urgentes primero)"""
    tareas_lista = []

    for codigo, info in tareas_colegio.items():
        fecha = string_a_fecha(info.get("fecha_fin", ""))
        # Si no puede parsear la fecha, la pone al final
        if fecha is None:
            fecha = string_a_fecha("31/12/9999")
        tareas_lista.append((fecha, codigo, info))

    # Ordenar por fecha
    tareas_lista.sort(key=lambda x: x[0])

    # Reconstruir el diccionario ordenado
    return {codigo: info for fecha, codigo, info in tareas_lista}

# ============================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================

def mostrar_lista_tareas(tareas_dict=None, titulo="LISTA DE TAREAS"):
    """Muestra una lista de tareas en formato tabla con indicadores de urgencia"""
    if tareas_dict is None:
        tareas_dict = tareas_colegio

    limpiar_pantalla()
    linea_separadora()
    print(f"  {titulo}")
    linea_separadora()

    if not tareas_dict:
        print("\nNo hay tareas para mostrar\n")
        return

    # Encabezados
    print(f"{'CODIGO':<8} {'MATERIA':<15} {'TAREA':<25} {'VENCE':<15} {'ESTADO':<12}")
    linea_separadora(80, "-")

    for codigo, info in sorted(tareas_dict.items()):
        materia = info.get("materia", "")[:14]
        tarea = info.get("tarea", "")[:24]
        estado = info.get("estado", "En proceso")

        # Calcular días restantes y obtener indicador
        dias = calcular_dias_restantes(info.get("fecha_fin", ""))
        urgencia = obtener_indicador_urgencia(dias)

        # Si la tarea está completada, mostrar indicador diferente
        if estado == "Completada":
            urgencia = "COMPLETADA"

        print(f"{codigo:<8} {materia:<15} {tarea:<25} {urgencia:<15} {estado:<12}")

    print(f"\nTotal: {len(tareas_dict)} tarea(s)")

def mostrar_detalle_tarea(codigo):
    """Muestra el detalle completo de una tarea"""
    tarea = obtener_tarea(codigo)
    if not tarea:
        print("\nNo existe una tarea con ese codigo")
        return

    print()
    linea_separadora(50)
    print(f"  DETALLE DE TAREA")
    linea_separadora(50)
    print(f"Codigo: {codigo}")
    print(f"Materia: {tarea['materia']}")
    print(f"Tarea: {tarea['tarea']}")
    print(f"Fecha inicio: {tarea['fecha_inicio']}")
    print(f"Fecha fin: {tarea['fecha_fin']}")

    # Mostrar días restantes si la tarea no está completada
    if tarea['estado'] == "En proceso":
        dias = calcular_dias_restantes(tarea['fecha_fin'])
        indicador = obtener_indicador_urgencia(dias)
        print(f"Tiempo restante: {indicador}")

    print(f"Estado: {tarea['estado']}")
    if tarea.get('observaciones'):
        print(f"Observaciones: {tarea['observaciones']}")
    linea_separadora(50)

# ============================================
# FUNCIONES DEL MENÚ
# ============================================

def opcion_agregar_tarea():
    """Agrega una nueva tarea"""
    limpiar_pantalla()
    linea_separadora(50)
    print("  AGREGAR NUEVA TAREA")
    linea_separadora(50)

    # Seleccionar materia
    materia = seleccionar_materia()
    if not materia:
        print("Operacion cancelada")
        return

    # Pedir descripción de la tarea
    tarea = input("\nDescripcion de la tarea: ").strip()
    if not tarea:
        print("La descripcion es obligatoria")
        return

    # Pedir fecha de inicio con validación
    while True:
        fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ").strip()
        if not fecha_inicio:
            print("La fecha de inicio es obligatoria")
            continue
        if not validar_fecha(fecha_inicio):
            print("Formato invalido. Use DD/MM/AAAA (ej: 15/11/2024)")
            continue
        break

    # Pedir fecha de fin/vencimiento con validación
    while True:
        fecha_fin = input("Fecha de vencimiento (DD/MM/AAAA): ").strip()
        if not fecha_fin:
            print("La fecha de vencimiento es obligatoria")
            continue
        if not validar_fecha(fecha_fin):
            print("Formato invalido. Use DD/MM/AAAA (ej: 20/11/2024)")
            continue

        # Validar que la fecha fin no sea anterior a la fecha inicio
        if string_a_fecha(fecha_fin) < string_a_fecha(fecha_inicio):
            print("La fecha de vencimiento no puede ser anterior a la fecha de inicio")
            continue
        break

    # Pedir observaciones (opcional)
    observaciones = input("Observaciones o notas (opcional): ").strip()

    # Agregar la tarea
    codigo = agregar_tarea(materia, tarea, fecha_inicio, fecha_fin, observaciones)

    print("\nTarea agregada exitosamente")
    print(f"Codigo asignado: {codigo}")

def opcion_ver_detalle():
    """Muestra el detalle de una tarea"""
    mostrar_lista_tareas()

    if not tareas_colegio:
        return

    codigo = input("\nIngrese el codigo de la tarea: ").strip().upper()
    mostrar_detalle_tarea(codigo)

def opcion_marcar_completada():
    """Marca una tarea como completada"""
    pendientes = obtener_tareas_pendientes()
    mostrar_lista_tareas(pendientes, "TAREAS PENDIENTES")

    if not pendientes:
        return

    codigo = input("\nCodigo de la tarea a completar: ").strip().upper()
    if marcar_completada(codigo):
        print("\nTarea completada! Bien hecho!")
    else:
        print("No se pudo completar la tarea (codigo invalido)")

def opcion_editar_tarea():
    """Edita una tarea existente"""
    mostrar_lista_tareas()

    if not tareas_colegio:
        return

    codigo = input("\nCodigo de la tarea a editar: ").strip().upper()
    tarea_info = obtener_tarea(codigo)

    if not tarea_info:
        print("No existe una tarea con ese codigo")
        return

    print("\n(Presione ENTER para mantener el valor actual)")

    # Editar campos
    nueva_tarea = input(f"Tarea [{tarea_info['tarea']}]: ").strip()
    if nueva_tarea:
        tarea_info['tarea'] = nueva_tarea

    nueva_fecha_inicio = input(f"Fecha inicio [{tarea_info['fecha_inicio']}]: ").strip()
    if nueva_fecha_inicio:
        if validar_fecha(nueva_fecha_inicio):
            tarea_info['fecha_inicio'] = nueva_fecha_inicio
        else:
            print("Formato invalido. Se mantiene la fecha actual")

    nueva_fecha_fin = input(f"Fecha vencimiento [{tarea_info['fecha_fin']}]: ").strip()
    if nueva_fecha_fin:
        if validar_fecha(nueva_fecha_fin):
            # Validar que no sea anterior a fecha inicio
            fecha_inicio_actual = tarea_info.get('fecha_inicio', '')
            if fecha_inicio_actual and string_a_fecha(nueva_fecha_fin) < string_a_fecha(fecha_inicio_actual):
                print("La fecha de vencimiento no puede ser anterior a la fecha de inicio")
            else:
                tarea_info['fecha_fin'] = nueva_fecha_fin
        else:
            print("Formato invalido. Se mantiene la fecha actual")

    nuevas_obs = input(f"Observaciones [{tarea_info.get('observaciones', '')}]: ").strip()
    if nuevas_obs:
        tarea_info['observaciones'] = nuevas_obs

    # Preguntar si quiere cambiar el estado
    if tarea_info['estado'] == "En proceso":
        cambiar_estado = input("Marcar como completada? (S/N): ").upper()
        if cambiar_estado == "S":
            tarea_info['estado'] = "Completada"
    else:
        cambiar_estado = input("Marcar como en proceso? (S/N): ").upper()
        if cambiar_estado == "S":
            tarea_info['estado'] = "En proceso"

    print("\nTarea actualizada correctamente")

def opcion_eliminar_tarea():
    """Elimina una tarea"""
    mostrar_lista_tareas()

    if not tareas_colegio:
        return

    codigo = input("\nCodigo de la tarea a eliminar: ").strip().upper()

    if codigo not in tareas_colegio:
        print("No existe una tarea con ese codigo")
        return

    confirmar = input("Esta seguro? (S/N): ").upper()
    if confirmar == "S":
        if eliminar_tarea(codigo):
            print("\nTarea eliminada")
    else:
        print("Operacion cancelada")

def opcion_borrar_todas():
    """Borra todas las tareas"""
    global tareas_colegio, siguiente_numero

    if not tareas_colegio:
        print("\nNo hay tareas para borrar")
        return

    print(f"\nSe eliminaran {len(tareas_colegio)} tarea(s)")
    confirmar = input("Esta seguro? (S/N): ").upper()

    if confirmar == "S":
        tareas_colegio = {}
        siguiente_numero = 1
        print("\nTodas las tareas fueron eliminadas")
    else:
        print("Operacion cancelada")

def submenu_ver_tareas():
    """Submenú para ver tareas"""
    opciones = {
        "1": ("Ver todas las tareas", lambda: mostrar_lista_tareas()),
        "2": ("Ver tareas pendientes", lambda: mostrar_lista_tareas(obtener_tareas_pendientes(), "TAREAS PENDIENTES")),
        "3": ("Ver tareas completadas", lambda: mostrar_lista_tareas(obtener_tareas_completadas(), "TAREAS COMPLETADAS")),
        "4": ("Ver tareas por fecha de vencimiento", lambda: mostrar_lista_tareas(obtener_tareas_ordenadas_por_fecha(), "TAREAS POR FECHA DE VENCIMIENTO")),
        "5": ("Ver detalle de una tarea", opcion_ver_detalle),
        "6": ("Volver al menu principal", None),
    }

    while True:
        limpiar_pantalla()
        linea_separadora()
        print("         VER TAREAS - SUBMENU")
        linea_separadora()

        for num, (descripcion, _) in opciones.items():
            print(f"{num}. {descripcion}")

        linea_separadora()

        opcion = input("\nSeleccione una opcion (1-6): ").strip()

        if opcion == "6":
            break

        if opcion in opciones and opciones[opcion][1]:
            try:
                opciones[opcion][1]()
                pausar()
            except Exception as e:
                print(f"\nError: {e}")
                pausar()
        else:
            print("\nOpcion no valida")
            pausar()

def ejecutar_menu_principal():
    """Ejecuta el menú principal del programa"""
    opciones = {
        "1": ("Agregar tarea", opcion_agregar_tarea),
        "2": ("Ver tareas", submenu_ver_tareas),
        "3": ("Marcar tarea como completada", opcion_marcar_completada),
        "4": ("Editar tarea", opcion_editar_tarea),
        "5": ("Eliminar tarea", opcion_eliminar_tarea),
        "6": ("Borrar todas las tareas", opcion_borrar_todas),
        "7": ("Salir", None),
    }

    while True:
        limpiar_pantalla()
        linea_separadora()
        print("         GESTOR DE TAREAS DEL COLEGIO")
        linea_separadora()
        print("\n                MENU PRINCIPAL\n")

        for num, (descripcion, _) in opciones.items():
            print(f"  {num}. {descripcion}")

        print()
        linea_separadora()

        opcion = input("\nSeleccione una opcion (1-7): ").strip()

        if opcion == "7":
            break

        if opcion in opciones and opciones[opcion][1]:
            try:
                opciones[opcion][1]()
                if opcion != "2":  # No pausar después del submenú
                    pausar()
            except Exception as e:
                print(f"\nError: {e}")
                pausar()
        else:
            print("\nOpcion no valida")
            pausar()