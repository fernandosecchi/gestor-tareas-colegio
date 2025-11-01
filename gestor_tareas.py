"""
GESTOR DE TAREAS DEL COLEGIO

UTILIDAD:
Este archivo contiene toda la lógica principal del sistema de gestión de tareas.
Maneja el almacenamiento en memoria, las operaciones CRUD (crear, leer, actualizar,
eliminar), la visualización de datos y el sistema de menús.

DEPENDENCIAS:
- materias.py: Necesario para seleccionar_materia(), que permite al usuario
  elegir una materia de una lista predefinida al crear tareas
- utils.py: Proporciona funciones auxiliares para:
  * limpiar_pantalla(): Limpia la consola para mejor visualización
  * pausar(): Detiene el flujo hasta que el usuario presione Enter
  * linea_separadora(): Dibuja líneas decorativas en la interfaz
  * validar_fecha(): Verifica que las fechas tengan formato DD/MM/AAAA
  * calcular_dias_restantes(): Calcula días hasta el vencimiento
  * obtener_indicador_urgencia(): Genera indicadores como [HOY], [MANANA], etc.
  * string_a_fecha(): Convierte texto a objeto fecha para comparaciones
"""

# Importación de la función para seleccionar materias desde el catálogo
from materias import seleccionar_materia

# Importación de todas las utilidades necesarias para la interfaz y fechas
from utils import (
    limpiar_pantalla, pausar, linea_separadora,
    validar_fecha, calcular_dias_restantes,
    obtener_indicador_urgencia, formatear_fecha_corta,
    string_a_fecha
)

# ============================================
# DATOS GLOBALES (en memoria)
# ============================================
# Diccionario principal que almacena todas las tareas {codigo: datos_tarea}
tareas_colegio = {}
# Contador para generar códigos únicos T001, T002, T003...
siguiente_numero = 1

# ============================================
# FUNCIONES DE GESTIÓN DE TAREAS
# ============================================

def obtener_tareas():
    """Devuelve todas las tareas"""
    # Retorna el diccionario completo de tareas
    return tareas_colegio

def generar_codigo():
    """Genera un código único con formato T001, T002, etc."""
    # Accede a la variable global para poder modificarla
    global siguiente_numero
    # Formatea el número con 3 dígitos (001, 002, 003...)
    codigo = f"T{siguiente_numero:03d}"
    # Incrementa el contador para el próximo código
    siguiente_numero += 1
    # Devuelve el código generado
    return codigo

def agregar_tarea(materia, tarea, fecha_inicio, fecha_fin, observaciones=""):
    """Agrega una nueva tarea con todos los campos requeridos"""
    # Genera un código único para esta nueva tarea
    codigo = generar_codigo()

    # Crea un diccionario con todos los datos de la tarea
    tareas_colegio[codigo] = {
        "materia": materia,              # Nombre de la asignatura
        "tarea": tarea,                  # Descripción de la tarea
        "fecha_inicio": fecha_inicio,    # Cuándo comenzar (DD/MM/AAAA)
        "fecha_fin": fecha_fin,          # Fecha de vencimiento (DD/MM/AAAA)
        "estado": "En proceso",          # Estado inicial (puede ser "Completada" después)
        "codigo": codigo,                # Código único de identificación
        "observaciones": observaciones   # Notas adicionales (opcional)
    }

    # Retorna el código asignado para confirmar al usuario
    return codigo

def obtener_tarea(codigo):
    """Obtiene una tarea por su código"""
    # Busca el código en el diccionario, devuelve None si no existe
    return tareas_colegio.get(codigo, None)

def marcar_completada(codigo):
    """Marca una tarea como completada"""
    # Verifica si el código existe en el diccionario
    if codigo in tareas_colegio:
        # Cambia el estado de "En proceso" a "Completada"
        tareas_colegio[codigo]["estado"] = "Completada"
        # Retorna True indicando éxito
        return True
    # Retorna False si no encontró la tarea
    return False

def eliminar_tarea(codigo):
    """Elimina una tarea"""
    # Verifica si el código existe
    if codigo in tareas_colegio:
        # Elimina la entrada del diccionario
        del tareas_colegio[codigo]
        # Retorna True indicando éxito
        return True
    # Retorna False si no encontró la tarea
    return False

def obtener_tareas_pendientes():
    """Devuelve solo las tareas en proceso"""
    # Crea un nuevo diccionario filtrando solo las tareas con estado "En proceso"
    return {cod: info for cod, info in tareas_colegio.items()
            if info.get("estado") == "En proceso"}

def obtener_tareas_completadas():
    """Devuelve solo las tareas completadas"""
    # Crea un nuevo diccionario filtrando solo las tareas con estado "Completada"
    return {cod: info for cod, info in tareas_colegio.items()
            if info.get("estado") == "Completada"}

def obtener_estadisticas():
    """Calcula estadísticas de las tareas"""
    # Cuenta el total de tareas en el diccionario
    total = len(tareas_colegio)
    # Cuenta cuántas tareas están completadas usando una expresión generadora
    completadas = sum(1 for t in tareas_colegio.values() if t.get("estado") == "Completada")
    # Calcula las pendientes por diferencia
    pendientes = total - completadas

    # Inicializa el porcentaje en 0
    porcentaje = 0
    # Solo calcula porcentaje si hay tareas para evitar división por cero
    if total > 0:
        porcentaje = (completadas / total) * 100

    # Retorna un diccionario con todas las estadísticas
    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "porcentaje_completado": porcentaje
    }

def obtener_tareas_ordenadas_por_fecha():
    """Devuelve las tareas ordenadas por fecha de vencimiento (más urgentes primero)"""
    # Lista temporal para almacenar tuplas (fecha, código, info)
    tareas_lista = []

    # Recorre todas las tareas del diccionario
    for codigo, info in tareas_colegio.items():
        # Convierte la fecha de texto a objeto fecha para poder ordenar
        fecha = string_a_fecha(info.get("fecha_fin", ""))
        # Si la fecha es inválida, la pone al final con una fecha muy lejana
        if fecha is None:
            fecha = string_a_fecha("31/12/9999")
        # Agrega la tupla a la lista
        tareas_lista.append((fecha, codigo, info))

    # Ordena la lista por el primer elemento de cada tupla (la fecha)
    tareas_lista.sort(key=lambda x: x[0])

    # Reconstruye un diccionario ordenado usando comprensión de diccionarios
    return {codigo: info for fecha, codigo, info in tareas_lista}

# ============================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================

def mostrar_lista_tareas(tareas_dict=None, titulo="LISTA DE TAREAS"):
    """Muestra una lista de tareas en formato tabla con indicadores de urgencia"""
    # Si no se pasa un diccionario específico, usa todas las tareas
    if tareas_dict is None:
        tareas_dict = tareas_colegio

    # Limpia la consola para una visualización limpia
    limpiar_pantalla()
    # Dibuja línea decorativa superior
    linea_separadora()
    # Imprime el título centrado
    print(f"  {titulo}")
    # Dibuja línea decorativa inferior
    linea_separadora()

    # Si no hay tareas, muestra mensaje y termina
    if not tareas_dict:
        print("\nNo hay tareas para mostrar\n")
        return

    # Imprime los encabezados de las columnas con formato fijo
    print(f"{'CODIGO':<8} {'MATERIA':<15} {'TAREA':<25} {'VENCE':<15} {'ESTADO':<12}")
    # Línea separadora más delgada para los encabezados
    linea_separadora(80, "-")

    # Itera sobre las tareas ordenadas por código
    for codigo, info in sorted(tareas_dict.items()):
        # Extrae y trunca la materia a 14 caracteres máximo
        materia = info.get("materia", "")[:14]
        # Extrae y trunca la descripción a 24 caracteres máximo
        tarea = info.get("tarea", "")[:24]
        # Obtiene el estado actual de la tarea
        estado = info.get("estado", "En proceso")

        # Calcula cuántos días faltan para el vencimiento
        dias = calcular_dias_restantes(info.get("fecha_fin", ""))
        # Obtiene el indicador textual ([HOY], [MANANA], etc.)
        urgencia = obtener_indicador_urgencia(dias)

        # Si la tarea está completada, sobrescribe el indicador
        if estado == "Completada":
            urgencia = "COMPLETADA"

        # Imprime la fila con formato de columnas alineadas
        print(f"{codigo:<8} {materia:<15} {tarea:<25} {urgencia:<15} {estado:<12}")

    # Muestra el total de tareas al final
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
    # Limpia la pantalla para mostrar el formulario
    limpiar_pantalla()
    # Dibuja el encabezado del formulario
    linea_separadora(50)
    print("  AGREGAR NUEVA TAREA")
    linea_separadora(50)

    # Llama a la función de materias.py para mostrar lista y seleccionar
    materia = seleccionar_materia()
    # Si el usuario cancela o no selecciona, termina la función
    if not materia:
        print("Operacion cancelada")
        return

    # Solicita la descripción de la tarea
    tarea = input("\nDescripcion de la tarea: ").strip()
    # Valida que no esté vacía
    if not tarea:
        print("La descripcion es obligatoria")
        return

    # Bucle para validar fecha de inicio
    while True:
        # Pide la fecha de inicio
        fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ").strip()
        # Verifica que no esté vacía
        if not fecha_inicio:
            print("La fecha de inicio es obligatoria")
            continue  # Vuelve a pedir
        # Valida el formato usando la función de utils.py
        if not validar_fecha(fecha_inicio):
            print("Formato invalido. Use DD/MM/AAAA (ej: 15/11/2024)")
            continue  # Vuelve a pedir
        break  # Sale del bucle si todo está bien

    # Bucle para validar fecha de vencimiento
    while True:
        # Pide la fecha de vencimiento
        fecha_fin = input("Fecha de vencimiento (DD/MM/AAAA): ").strip()
        # Verifica que no esté vacía
        if not fecha_fin:
            print("La fecha de vencimiento es obligatoria")
            continue
        # Valida el formato
        if not validar_fecha(fecha_fin):
            print("Formato invalido. Use DD/MM/AAAA (ej: 20/11/2024)")
            continue

        # Convierte ambas fechas a objetos fecha para compararlas
        if string_a_fecha(fecha_fin) < string_a_fecha(fecha_inicio):
            print("La fecha de vencimiento no puede ser anterior a la fecha de inicio")
            continue  # Vuelve a pedir si la fecha es inválida
        break  # Sale del bucle si todo está bien

    # Campo opcional para notas adicionales
    observaciones = input("Observaciones o notas (opcional): ").strip()

    # Llama a la función que guarda la tarea en el diccionario
    codigo = agregar_tarea(materia, tarea, fecha_inicio, fecha_fin, observaciones)

    # Muestra confirmación con el código asignado
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