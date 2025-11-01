# CLAUDE.md

Este archivo proporciona orientación para Claude Code al trabajar con este repositorio.

## Descripción del Proyecto

Sistema ultra-simplificado de gestión de tareas escolares en Python. Las tareas solo existen en memoria durante la ejecución del programa - no hay persistencia de datos.

## Estructura de Datos de Tarea

Cada tarea contiene **7 campos obligatorios**:

```python
{
    "materia": "Matematicas",           # Asignatura
    "tarea": "Resolver ejercicios",      # Descripción de la tarea
    "fecha_inicio": "01/11/2024",        # Fecha de inicio
    "fecha_fin": "05/11/2024",           # Fecha de vencimiento
    "estado": "En proceso",              # "En proceso" o "Completada"
    "codigo": "T001",                    # Código único generado
    "observaciones": "Notas adicionales" # Observaciones o notas
}
```

## Estructura del Sistema

El proyecto consta de **4 archivos Python**:

### 1. main.py (23 líneas)
- Punto de entrada del programa
- Maneja el ciclo de vida de la aplicación

### 2. gestor_tareas.py (~350 líneas)
- Lógica de negocio principal
- Gestión CRUD de tareas
- Sistema de menús y submenús

### 3. materias.py (60 líneas)
- Catálogo de materias predefinidas
- Función de selección de materias

### 4. utils.py (43 líneas)
- Funciones utilitarias comunes
- limpiar_pantalla(), pausar(), linea_separadora()
- mostrar_despedida()

## Diccionario Principal

```python
tareas_colegio = {
    "T001": {
        "materia": "Matematicas",
        "tarea": "Resolver ejercicios cap 5",
        "fecha_inicio": "01/11/2024",
        "fecha_fin": "05/11/2024",
        "estado": "En proceso",
        "codigo": "T001",
        "observaciones": "Repasar formulas"
    },
    "T002": {...}
}
```

## Flujo de Estados

- **Estado inicial**: "En proceso" (al crear tarea)
- **Estado final**: "Completada" (al marcar como completada)
- Se puede cambiar entre estados mediante edición

## Funciones Principales

### Agregar Tarea
```python
codigo = agregar_tarea(
    materia="Matematicas",
    tarea="Descripcion",
    fecha_inicio="01/11/2024",
    fecha_fin="05/11/2024",
    observaciones="Notas"
)
```

### Filtros de Estado
- `obtener_tareas_pendientes()` - Tareas con estado "En proceso"
- `obtener_tareas_completadas()` - Tareas con estado "Completada"

## Menú del Sistema

1. Agregar tarea (pide todos los campos)
2. Ver tareas → Submenú
3. Marcar tarea como completada
4. Editar tarea (puede modificar todos los campos)
5. Eliminar tarea
6. Borrar todas las tareas
7. Salir

## Características

- **Sin persistencia**: Todo en memoria
- **Código único**: T001, T002, T003...
- **7 campos por tarea**: Todos obligatorios excepto observaciones
- **Sin emojis**: Interfaz de texto puro
- **Estados claros**: "En proceso" o "Completada"

## Testing Rápido

```python
import gestor_tareas as gt

# Agregar tarea con todos los campos
codigo = gt.agregar_tarea(
    materia="Fisica",
    tarea="Laboratorio de optica",
    fecha_inicio="01/11/2024",
    fecha_fin="08/11/2024",
    observaciones="Llevar bata blanca"
)

# Ver tarea
tarea = gt.obtener_tarea(codigo)
print(tarea)  # Muestra todos los 7 campos

# Cambiar estado
gt.marcar_completada(codigo)
```

## Notas Importantes

- **7 campos por tarea**: materia, tarea, fecha_inicio, fecha_fin, estado, codigo, observaciones
- **Estados**: Solo "En proceso" o "Completada"
- **Sin persistencia**: Todo es temporal
- **Códigos secuenciales**: T001, T002, T003...
- **Interface limpia**: Sin emojis, texto puro