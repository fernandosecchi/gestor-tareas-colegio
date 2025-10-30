#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE MENÚ Y NAVEGACIÓN
================================================

Este módulo implementa la interfaz de usuario por consola (CLI).
Actúa como capa de presentación y controlador de flujo de la aplicación.

Responsabilidades del módulo:
- Renderizado de menús y formularios en consola
- Captura y validación de entrada del usuario
- Coordinación entre módulos (tareas, archivo, vistas)
- Control del bucle principal de la aplicación
- Manejo de errores de entrada del usuario

Conceptos técnicos aplicados:
- Bucle de eventos (event loop) para menú interactivo
- Validación de entrada con bucles while
- Separación de responsabilidades (MVC-like)
- Manejo de excepciones de conversión de tipos
- Funciones de alto nivel que orquestan operaciones
"""

# Importamos los módulos que necesitamos
import tareas
import materias
import archivo
import vistas
import utils


# ============================================
# FUNCIONES DE MENÚ PRINCIPAL
# ============================================

def mostrar_menu_principal():
    """
    Muestra el menú principal con todas las opciones.
    """
    # Mostramos el menú
    utils.limpiar_pantalla()
    print("=" * 60)
    print("         📚 GESTOR DE TAREAS DEL COLEGIO 📚")
    print("=" * 60)
    print("1. ➕ Agregar tarea")
    print("2. 🔎 Ver detalle de tarea")
    print("3. 📋 Ver todas las tareas")
    print("4. ⏰ Ver tareas pendientes")
    print("5. ✅ Ver tareas completadas")
    print("6. 🔍 Buscar tarea")
    print("7. ✏️  Editar tarea")
    print("8. 🗑️  Eliminar tarea")
    print("9. 🧹 Borrar todas las tareas")
    print("10. 🚪 Salir")
    print("=" * 60)


def procesar_opcion_menu(opcion):
    """
    Procesa la opción seleccionada del menú.
    
    Args:
        opcion (str): Opción seleccionada
        
    Returns:
        bool: True si debe continuar, False si debe salir
    """
    if opcion == "1":
        utils.limpiar_pantalla()
        opcion_agregar_tarea()
        
    elif opcion == "2":
        utils.limpiar_pantalla()
        opcion_ver_detalle_tarea()
        
    elif opcion == "3":
        utils.limpiar_pantalla()
        vistas.mostrar_todas_las_tareas()
        
    elif opcion == "4":
        utils.limpiar_pantalla()
        vistas.mostrar_tareas_pendientes()
        
    elif opcion == "5":
        utils.limpiar_pantalla()
        opcion_ver_completadas()
        
    elif opcion == "6":
        utils.limpiar_pantalla()
        opcion_buscar_tarea()
        
    elif opcion == "7":
        utils.limpiar_pantalla()
        opcion_editar_tarea()
        
    elif opcion == "8":
        utils.limpiar_pantalla()
        opcion_eliminar_tarea()
        
    elif opcion == "9":
        utils.limpiar_pantalla()
        opcion_borrar_todas()
        
    elif opcion == "10":
        return False  # Señal para salir
        
    else:
        print("\n❌ Opción no válida. Por favor, elija un número del 1 al 10.")
    
    return True  # Continuar en el menú


def ejecutar_menu_principal():
    """
    Bucle principal del menú interactivo.
    
    Mantiene la aplicación activa hasta que el usuario elija salir.
    En cada iteración: muestra el menú, procesa la selección y hace una pausa.
    """
    continuar = True
    
    # Bucle infinito controlado por la variable 'continuar'
    while continuar:
        # Paso 1: Mostramos el menú
        mostrar_menu_principal()
        
        # Paso 2: Capturamos la elección del usuario
        opcion = input("\n📝 Seleccione una opción (1-10): ").strip()
        
        # Paso 3: Procesamos la opción y obtenemos si debe continuar
        continuar = procesar_opcion_menu(opcion)
        
        # Paso 4: Pausa para que el usuario lea los resultados
        # Solo pausamos si vamos a continuar (no al salir)
        if continuar:
            utils.pausar()


# ============================================
# FUNCIONES DE OPCIONES ESPECÍFICAS
# ============================================

def opcion_agregar_tarea():
    """
    Gestiona el flujo de creación de una nueva tarea.
    
    Solicita al usuario los datos necesarios y crea la tarea:
    - Materia
    - Tarea (descripción)
    - Fecha inicio (opcional)
    - Fecha fin / vencimiento (obligatoria)
    - Estado (proceso o completada)
    - Código (automático, vinculado al ID) [informativo]
    - Observaciones (opcional)
    """
    print("\n" + "=" * 50)
    print("         ➥ AGREGAR NUEVA TAREA")
    print("=" * 50)
    
    # Paso 1: Selección de materia
    materia = materias.seleccionar_materia()
    
    # Paso 2: Solicitud y validación de la descripción
    print("\n📝 TAREA (DESCRIPCIÓN):")
    print("   (Ejemplo: Resolver ejercicios 1 al 10 de la página 45)")
    descripcion = input("   ➡️ ").strip()
    while not descripcion:
        print("❌ La descripción no puede estar vacía")
        descripcion = input("   ➡️ ").strip()
    
    # Paso 3: Fechas
    print("\n📅 FECHA INICIO (opcional):")
    fecha_inicio = input("   ➡️ ").strip()
    
    print("\n📅 FECHA FIN / VENCIMIENTO:")
    print("   (Ejemplos: Lunes, Mañana, 15 de marzo, Próxima semana)")
    fecha_fin = input("   ➡️ ").strip()
    while not fecha_fin:
        print("❌ La fecha de fin no puede estar vacía")
        fecha_fin = input("   ➡️ ").strip()
    
    # Paso 4: Estado
    print("\n⏱️ ESTADO DE LA TAREA: Proceso o Completada")
    estado_raw = input("   (P=Proceso, C=Completada) [P]: ").strip().upper()
    if estado_raw == "":
        estado_raw = "P"
    while estado_raw not in ("P", "C", "PROCESO", "COMPLETADA"):
        print("❌ Opción no válida. Ingrese P o C (o escriba Proceso/Completada)")
        estado_raw = input("   (P=Proceso, C=Completada) [P]: ").strip().upper() or "P"
    completada = estado_raw in ("C", "COMPLETADA")
    
    # Paso 5: Observaciones
    print("\n🗒️ OBSERVACIONES / NOTAS (opcional):")
    observaciones = input("   ➡️ ").strip()
    
    # Paso 6: Creación de la tarea en el sistema
    id_creado = tareas.agregar_tarea(
        materia=materia,
        descripcion=descripcion,
        fecha_fin=fecha_fin,
        fecha_inicio=fecha_inicio,
        completada=completada,
        observaciones=observaciones,
    )
    
    # Paso 7: Confirmación visual al usuario
    info_creada = tareas.obtener_tarea(id_creado) or {}
    codigo_generado = info_creada.get("codigo", "")
    print("\n" + "=" * 50)
    print("✅ TAREA AGREGADA EXITOSAMENTE")
    print("=" * 50)
    print(f"📌 ID de la tarea: {id_creado}")
    if codigo_generado:
        print(f"🔖 Código: {codigo_generado}")
    print(f"📚 Materia: {materia}")
    print(f"📝 Descripción: {descripcion}")
    if fecha_inicio:
        print(f"🗓️ Fecha inicio: {fecha_inicio}")
    print(f"📅 Fecha fin: {fecha_fin}")
    print(f"Estado: {'Completada' if completada else 'En proceso'}")
    if observaciones:
        print(f"🗒️ Observaciones: {observaciones}")
    print("=" * 50)
    
    # Paso 8: Persistencia automática de cambios
    archivo.guardar_tareas()


def opcion_ver_por_materia():
    """
    Maneja la opción de ver tareas por materia.
    """
    print("\n" + "=" * 50)
    print("         🔍 VER TAREAS POR MATERIA")
    print("=" * 50)
    
    # Verificamos si hay tareas
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas registradas")
        return
    
    # Seleccionamos la materia
    materia_buscar = materias.seleccionar_materia()
    
    # Obtenemos las tareas de esa materia
    tareas_materia = tareas.obtener_tareas_por_materia(materia_buscar)
    
    # Mostramos los resultados
    vistas.mostrar_tareas_materia(materia_buscar, tareas_materia)


def opcion_marcar_completada():
    """
    Gestiona el proceso de marcar una tarea como completada.
    
    Muestra las tareas pendientes, solicita la selección del usuario,
    actualiza el estado y persiste los cambios.
    """
    print("\n" + "=" * 50)
    print("         ✅ MARCAR TAREA COMO COMPLETADA")
    print("=" * 50)
    
    # Obtenemos solo las tareas que están pendientes
    pendientes = tareas.obtener_tareas_pendientes()
    
    # Validación inicial: verificamos que haya tareas por completar
    if not pendientes:
        print("\n🎉 ¡Felicitaciones! No hay tareas pendientes")
        return
    
    # Mostramos listado de tareas pendientes
    print("\n📋 TAREAS PENDIENTES:")
    print("-" * 40)
    
    for id_tarea, info in pendientes.items():
        print(f"\n  📌 Tarea #{id_tarea}")
        print(f"     {info['materia']}: {info['descripcion']}")
        print(f"     📅 Entregar: {info['fecha_fin']}")
    
    print("\n" + "-" * 40)
    
    # Bucle de selección con validación de entrada
    while True:
        try:
            id_elegido = int(input("📝 Ingrese el ID de la tarea completada (0 para cancelar): "))
            
            # Opción de cancelación
            if id_elegido == 0:
                print("❌ Operación cancelada")
                return
            
            # Verificamos que el ID exista en pendientes
            if id_elegido in pendientes:
                # Actualizamos el estado de la tarea
                if tareas.marcar_completada(id_elegido):
                    tarea_info = tareas.obtener_tarea(id_elegido)
                    
                    # Confirmación visual al usuario
                    print("\n" + "=" * 50)
                    print("🎉 ¡EXCELENTE! TAREA COMPLETADA")
                    print("=" * 50)
                    print(f"✅ Tarea #{id_elegido}")
                    print(f"   {tarea_info['materia']}")
                    print(f"   {tarea_info['descripcion']}")
                    print("\n¡Sigue así! 💪")
                    
                    # Persistimos los cambios
                    archivo.guardar_tareas()
                    return
            else:
                print("❌ ID no válido o tarea ya completada")
                
        except ValueError:
            # Manejo de error: el usuario no ingresó un número
            print("❌ Debe ingresar un número válido")


def opcion_ver_detalle_tarea():
    """
    Muestra el detalle de una tarea por ID.
    """
    print("\n" + "=" * 50)
    print("         🔎 VER DETALLE DE TAREA")
    print("=" * 50)
    
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas registradas")
        return
    
    try:
        texto = input("📝 Ingrese el ID de la tarea: ").strip()
        if not utils.es_entero_valido(texto):
            print("❌ Debe ingresar un número válido")
            return
        id_buscar = int(texto)
        info = tareas.obtener_tarea(id_buscar)
        if not info:
            print("❌ No existe una tarea con ese ID")
            return
        simbolo = "✅" if info.get("completada") else "⏰"
        print(f"\n{simbolo} Tarea #{id_buscar}")
        print(f"📚 Materia: {info.get('materia','')}")
        print(f"📝 Descripción: {info.get('descripcion','')}")
        # Fechas
        fi = info.get('fecha_inicio', '')
        ff = info.get('fecha_fin', '')
        if fi:
            print(f"🗓️ Fecha inicio: {fi}")
        if ff:
            print(f"📅 Fecha fin: {ff}")
        # Estado
        print(f"Estado: {'Completada' if info.get('completada') else 'En proceso'}")
        # Código y observaciones
        if info.get('codigo'):
            print(f"🔖 Código: {info.get('codigo')}")
        if info.get('observaciones'):
            print(f"🗒️ Observaciones: {info.get('observaciones')}")
    except Exception:
        print("❌ Error al leer el ID")


def opcion_ver_completadas():
    """
    Lista solo las tareas completadas.
    """
    print("\n" + "=" * 60)
    print("         ✅ TAREAS COMPLETADAS")
    print("=" * 60)
    completadas = tareas.obtener_tareas_completadas()
    if not completadas:
        print("\n📝 No hay tareas completadas todavía")
        return
    for id_tarea, info in completadas.items():
        print(f"\n✅ Tarea #{id_tarea}")
        print(f"   {info['materia']}: {info['descripcion']}")


def opcion_buscar_tarea():
    """
    Buscar tarea por ID o por texto (materia/descripcion).
    """
    print("\n" + "=" * 60)
    print("         🔍 BUSCAR TAREA")
    print("=" * 60)
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas registradas")
        return
    texto = input("📝 Ingrese ID o texto a buscar: ").strip()
    if not texto:
        print("❌ Debe ingresar un valor de búsqueda")
        return
    resultados = {}
    # Si es un número entero, intentamos por ID
    if utils.es_entero_valido(texto):
        id_posible = int(texto)
        info = tareas.obtener_tarea(id_posible)
        if info:
            resultados[id_posible] = info
    # Búsqueda por texto en materia o descripción (insensible a mayúsculas)
    consulta = texto.lower()
    for id_tarea, info in tareas.obtener_tareas().items():
        if consulta in info['materia'].lower() or consulta in info['descripcion'].lower():
            resultados[id_tarea] = info
    if not resultados:
        print("\n🔎 No se encontraron coincidencias")
        return
    print("\n📋 RESULTADOS:")
    print("-" * 40)
    for id_tarea, info in resultados.items():
        simbolo = "✅" if info["completada"] else "⏰"
        desc = utils.truncar_texto(info['descripcion'], 40)
        print(f"{simbolo} #{id_tarea} - {info['materia']}: {desc}")


def opcion_editar_tarea():
    """
    Edita los campos de una tarea existente.
    """
    print("\n" + "=" * 60)
    print("         ✏️  EDITAR TAREA")
    print("=" * 60)
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas para editar")
        return
    try:
        texto = input("📝 Ingrese el ID de la tarea a editar: ").strip()
        if not utils.es_entero_valido(texto):
            print("❌ Debe ingresar un número válido")
            return
        id_editar = int(texto)
        info = tareas.obtener_tarea(id_editar)
        if not info:
            print("❌ No existe una tarea con ese ID")
            return
        # Mostrar actual y pedir nuevos valores (enter para mantener)
        print(f"\nActual: Materia = {info['materia']}")
        print("Ingrese una nueva materia o presione ENTER para mantener:")
        nueva_materia = input("➡️ ").strip()
        if nueva_materia:
            # permitir seleccionar desde listado si desea
            if nueva_materia == "?":
                nueva_materia = materias.seleccionar_materia()
            info['materia'] = nueva_materia
        print(f"\nActual: Descripción = {info['descripcion']}")
        nueva_desc = input("Nueva descripción (ENTER para mantener): ").strip()
        if nueva_desc:
            info['descripcion'] = nueva_desc
        # Fechas
        actual_fi = info.get('fecha_inicio', '')
        actual_ff = info.get('fecha_fin', '')
        print(f"\nActual: Fecha inicio = {actual_fi}")
        nueva_fi = input("Nueva fecha inicio (ENTER para mantener): ").strip()
        if nueva_fi:
            info['fecha_inicio'] = nueva_fi
        print(f"\nActual: Fecha fin = {actual_ff}")
        nueva_ff = input("Nueva fecha fin (ENTER para mantener): ").strip()
        if nueva_ff:
            info['fecha_fin'] = nueva_ff
        # Permitir cambiar estado
        estado_actual = "S" if info['completada'] else "N"
        resp = input(f"\n¿Marcar como completada? (S/N, actual {estado_actual}): ").strip().upper()
        if resp == "S":
            info['completada'] = True
        elif resp == "N":
            info['completada'] = False
        # Código automático (solo informativo) y observaciones
        print(f"\nCódigo (automático, vinculado al ID): {info.get('codigo', '')}")
        print(f"\nActual: Observaciones = {info.get('observaciones', '')}")
        nuevas_obs = input("Nuevas observaciones (ENTER para mantener): ").strip()
        if nuevas_obs:
            info['observaciones'] = nuevas_obs
        # Guardar cambios
        archivo.guardar_tareas()
        print("\n✅ Tarea actualizada correctamente")
    except Exception:
        print("❌ Error durante la edición")


def opcion_borrar_todas():
    """
    Elimina todas las tareas tras confirmación.
    """
    print("\n" + "=" * 60)
    print("         🧹 BORRAR TODAS LAS TAREAS")
    print("=" * 60)
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas para borrar")
        return
    confirmar = input("⚠️ ¿Confirma borrar TODAS las tareas? (S/N): ").strip().upper()
    if confirmar == "S":
        # Vaciar el diccionario de tareas y reiniciar IDs de forma segura
        actuales = tareas.obtener_tareas()
        actuales.clear()
        # Reiniciar contador siguiente_id indirectamente
        tareas.establecer_tareas({})
        archivo.guardar_tareas()
        print("\n✅ Todas las tareas fueron eliminadas")
    else:
        print("❌ Operación cancelada")


def opcion_eliminar_tarea():
    """
    Maneja la opción de eliminar una tarea.
    """
    print("\n" + "=" * 50)
    print("         🗑️ ELIMINAR TAREA")
    print("=" * 50)
    
    # Verificamos si hay tareas
    if not tareas.hay_tareas():
        print("\n📭 No hay tareas para eliminar")
        return
    
    # Mostramos todas las tareas
    todas_tareas = tareas.obtener_tareas()
    print("\n📋 LISTA DE TAREAS:")
    print("-" * 40)
    
    for id_tarea, info in todas_tareas.items():
        simbolo = "✅" if info["completada"] else "⏰"
        descripcion_corta = utils.truncar_texto(info['descripcion'], 30)
        print(f"  {simbolo} #{id_tarea} - {info['materia']}: {descripcion_corta}")
    
    print("-" * 40)
    
    # Pedimos el ID
    while True:
        try:
            id_eliminar = int(input("\n📝 ID de la tarea a eliminar (0 para cancelar): "))
            
            if id_eliminar == 0:
                print("❌ Operación cancelada")
                return
            
            if id_eliminar in todas_tareas:
                # Mostramos la tarea a eliminar
                info = todas_tareas[id_eliminar]
                print("\n⚠️ VAS A ELIMINAR:")
                print(f"   Tarea #{id_eliminar}")
                print(f"   {info['materia']}: {info['descripcion']}")
                
                # Pedimos confirmación
                confirmar = input("\n¿Estás seguro? (S/N): ").upper().strip()
                
                if confirmar == "S":
                    if tareas.eliminar_tarea(id_eliminar):
                        print("\n✅ Tarea eliminada correctamente")
                        archivo.guardar_tareas()
                else:
                    print("❌ Operación cancelada")
                
                return
            else:
                print("❌ No existe una tarea con ese ID")
                
        except ValueError:
            print("❌ Debe ingresar un número válido")
