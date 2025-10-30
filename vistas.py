#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================
        MÓDULO DE VISTAS
================================================

Este módulo se encarga de mostrar información
en pantalla de forma organizada y atractiva.

Responsabilidades:
- Formatear la salida de datos
- Mostrar tareas en diferentes formatos
- Generar reportes visuales
- Crear barras de progreso y estadísticas

Conceptos que aprenderás:
- Formateo de strings
- Presentación de datos
- Creación de tablas en consola
- Visualización de estadísticas
"""

import tareas


# ============================================
# FUNCIONES DE VISUALIZACIÓN DE TAREAS
# ============================================

def mostrar_todas_las_tareas():
    """
    Muestra todas las tareas organizadas por estado.
    Primero las pendientes, luego las completadas.
    """
    print("\n" + "=" * 60)
    print("         📋 TODAS LAS TAREAS")
    print("=" * 60)
    
    # Obtenemos todas las tareas
    todas = tareas.obtener_tareas()
    
    if not todas:
        print("\n📭 No hay tareas registradas todavía")
        print("   Usa la opción 1 para agregar tu primera tarea")
        return
    
    # Obtenemos tareas separadas por estado
    pendientes = tareas.obtener_tareas_pendientes()
    completadas = tareas.obtener_tareas_completadas()
    
    # Mostramos tareas pendientes
    print("\n🔴 TAREAS PENDIENTES:")
    print("-" * 50)
    
    if pendientes:
        for id_tarea, info in pendientes.items():
            print(f"\n  📌 Tarea #{id_tarea}")
            print(f"     Materia: {info['materia']}")
            print(f"     Descripción: {info['descripcion']}")
            print(f"     📅 Entregar: {info['fecha_fin']}")
    else:
        print("  🎉 ¡No hay tareas pendientes! ¡Excelente!")
    
    # Mostramos tareas completadas
    print("\n\n🟢 TAREAS COMPLETADAS:")
    print("-" * 50)
    
    if completadas:
        for id_tarea, info in completadas.items():
            print(f"\n  ✅ Tarea #{id_tarea}")
            print(f"     Materia: {info['materia']}")
            print(f"     Descripción: {info['descripcion']}")
    else:
        print("  📝 No hay tareas completadas todavía")
    
    # Mostramos resumen
    mostrar_resumen_estadisticas()


def mostrar_tareas_pendientes():
    """
    Muestra solo las tareas pendientes, agrupadas por materia.
    """
    print("\n" + "=" * 60)
    print("         ⏰ TAREAS PENDIENTES")
    print("=" * 60)
    
    # Obtenemos las tareas pendientes
    pendientes = tareas.obtener_tareas_pendientes()
    
    if not pendientes:
        print("\n" + "🎉" * 10)
        print("  ¡FELICITACIONES!")
        print("  No tienes tareas pendientes")
        print("  Disfruta tu tiempo libre 😊")
        print("🎉" * 10)
        return
    
    # Agrupamos por materia
    por_materia = {}
    for id_tarea, info in pendientes.items():
        materia = info["materia"]
        if materia not in por_materia:
            por_materia[materia] = []
        
        por_materia[materia].append({
            "id": id_tarea,
            "descripcion": info["descripcion"],
            "fecha": info["fecha_fin"]
        })
    
    # Mostramos agrupadas y ordenadas
    total_pendientes = 0
    
    for materia in sorted(por_materia.keys()):
        lista_tareas = por_materia[materia]
        cantidad = len(lista_tareas)
        total_pendientes += cantidad
        
        print(f"\n📚 {materia} ({cantidad} tarea{'s' if cantidad > 1 else ''}):")
        print("-" * 40)
        
        for tarea in lista_tareas:
            print(f"  📌 Tarea #{tarea['id']}")
            print(f"     {tarea['descripcion']}")
            print(f"     📅 Entregar: {tarea['fecha']}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 TOTAL: {total_pendientes} tarea{'s' if total_pendientes > 1 else ''} pendiente{'s' if total_pendientes > 1 else ''}")
    print("=" * 60)


def mostrar_tareas_materia(nombre_materia, tareas_materia):
    """
    Muestra las tareas de una materia específica.
    
    Args:
        nombre_materia (str): Nombre de la materia
        tareas_materia (dict): Diccionario con las tareas de esa materia
    """
    print(f"\n📚 TAREAS DE: {nombre_materia.upper()}")
    print("=" * 50)
    
    if not tareas_materia:
        print(f"\n❌ No hay tareas de {nombre_materia}")
        return
    
    # Contadores
    completadas = 0
    pendientes = 0
    
    # Mostramos cada tarea
    for id_tarea, info in tareas_materia.items():
        if info["completada"]:
            simbolo = "✅"
            estado = "COMPLETADA"
            completadas += 1
        else:
            simbolo = "⏰"
            estado = "PENDIENTE"
            pendientes += 1
        
        print(f"\n  {simbolo} Tarea #{id_tarea} - {estado}")
        print(f"     Descripción: {info['descripcion']}")
        print(f"     📅 Fecha: {info['fecha_fin']}")
    
    # Resumen
    print("\n" + "-" * 50)
    print(f"📊 Resumen de {nombre_materia}:")
    print(f"   Total: {len(tareas_materia)} tarea(s)")
    print(f"   ✅ Completadas: {completadas}")
    print(f"   ⏰ Pendientes: {pendientes}")
    
    if len(tareas_materia) > 0:
        porcentaje = (completadas / len(tareas_materia)) * 100
        print(f"   📈 Progreso: {porcentaje:.1f}%")


# ============================================
# FUNCIONES DE ESTADÍSTICAS
# ============================================

def mostrar_resumen_estadisticas():
    """
    Muestra un resumen con estadísticas básicas.
    """
    stats = tareas.obtener_estadisticas()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Total de tareas: {stats['total']}")
    print(f"   ✅ Completadas: {stats['completadas']}")
    print(f"   ⏰ Pendientes: {stats['pendientes']}")
    
    # Barra de progreso
    if stats['total'] > 0:
        print(f"   📈 Progreso: {stats['porcentaje']:.1f}%")
        
        # Creamos la barra visual
        barra = crear_barra_progreso(stats['porcentaje'])
        print(f"   {barra}")
    
    print("=" * 60)


def mostrar_estadisticas_detalladas():
    """
    Muestra estadísticas detalladas del sistema.
    """
    print("\n" + "=" * 60)
    print("         📊 ESTADÍSTICAS DETALLADAS")
    print("=" * 60)
    
    # Obtenemos las estadísticas
    stats = tareas.obtener_estadisticas()
    
    if stats['total'] == 0:
        print("\n📭 No hay tareas registradas para generar estadísticas")
        return
    
    # Estadísticas generales
    print("\n📈 ESTADÍSTICAS GENERALES:")
    print("-" * 40)
    print(f"Total de tareas: {stats['total']}")
    print(f"Tareas completadas: {stats['completadas']}")
    print(f"Tareas pendientes: {stats['pendientes']}")
    print(f"Porcentaje completado: {stats['porcentaje']:.1f}%")
    
    # Barra de progreso grande
    print("\nPROGRESO GENERAL:")
    barra = crear_barra_progreso(stats['porcentaje'], 40)
    print(barra)
    
    # Estadísticas por materia
    if stats['por_materia']:
        print("\n📚 ESTADÍSTICAS POR MATERIA:")
        print("-" * 40)
        
        # Ordenamos por total de tareas (de mayor a menor)
        materias_ordenadas = sorted(
            stats['por_materia'].items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        for materia, datos in materias_ordenadas:
            total = datos['total']
            completadas = datos['completadas']
            pendientes = datos['pendientes']
            porcentaje = (completadas / total * 100) if total > 0 else 0
            
            print(f"\n{materia}:")
            print(f"  Total: {total} | Completadas: {completadas} | Pendientes: {pendientes}")
            
            # Mini barra de progreso
            mini_barra = crear_barra_progreso(porcentaje, 20)
            print(f"  {mini_barra} {porcentaje:.0f}%")
    
    # Información adicional
    mostrar_info_adicional()


def crear_barra_progreso(porcentaje, longitud=20):
    """
    Crea una barra de progreso visual.
    
    Args:
        porcentaje (float): Porcentaje de progreso (0-100)
        longitud (int): Longitud de la barra en caracteres
        
    Returns:
        str: Barra de progreso visual
    """
    # Calculamos cuántos caracteres llenar
    caracteres_llenos = int(porcentaje * longitud / 100)
    caracteres_vacios = longitud - caracteres_llenos
    
    # Creamos la barra
    barra = "█" * caracteres_llenos + "░" * caracteres_vacios
    
    return f"[{barra}]"


def mostrar_info_adicional():
    """
    Muestra información adicional como tips o mensajes motivacionales.
    """
    stats = tareas.obtener_estadisticas()
    
    print("\n" + "=" * 60)
    print("💡 INFORMACIÓN ADICIONAL:")
    print("-" * 40)
    
    # Mensajes según el estado
    if stats['pendientes'] == 0:
        print("🎉 ¡Excelente! No tienes tareas pendientes.")
        print("   Aprovecha para descansar o adelantar futuros trabajos.")
    elif stats['pendientes'] <= 3:
        print("👍 ¡Muy bien! Tienes pocas tareas pendientes.")
        print("   Con un poco de esfuerzo las terminarás pronto.")
    elif stats['pendientes'] <= 7:
        print("📝 Tienes varias tareas pendientes.")
        print("   Organiza tu tiempo y trabaja de forma constante.")
    else:
        print("⚠️ Tienes muchas tareas pendientes.")
        print("   Prioriza las más urgentes y divide el trabajo en partes.")
    
    # Si hay materias con muchas tareas
    if stats['por_materia']:
        materia_max = max(stats['por_materia'].items(), key=lambda x: x[1]['pendientes'])
        if materia_max[1]['pendientes'] > 3:
            print(f"\n📚 {materia_max[0]} tiene {materia_max[1]['pendientes']} tareas pendientes.")
            print("   Considera dedicarle más tiempo a esta materia.")
    
    print("=" * 60)


def mostrar_tabla_tareas():
    """
    Muestra las tareas en formato de tabla.
    Útil para una vista compacta.
    """
    todas = tareas.obtener_tareas()
    
    if not todas:
        print("No hay tareas para mostrar")
        return
    
    # Encabezados
    print("\n" + "=" * 80)
    print(f"{'ID':^5} | {'Materia':^15} | {'Descripción':^35} | {'Fecha':^15} | {'Estado':^8}")
    print("=" * 80)
    
    # Filas
    for id_tarea, info in todas.items():
        materia = info['materia'][:15]  # Truncamos si es muy largo
        descripcion = info['descripcion'][:35]
        fecha = info['fecha_fin'][:15]
        estado = "✅" if info['completada'] else "⏰"
        
        print(f"{id_tarea:^5} | {materia:^15} | {descripcion:<35} | {fecha:^15} | {estado:^8}")
    
    print("=" * 80)
