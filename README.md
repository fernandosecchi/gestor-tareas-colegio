# Gestor de Tareas del Colegio 📚

Una aplicación de consola en Python para gestionar tareas escolares de manera eficiente y organizada.

## Características ✨

- **Gestión completa de tareas**: Crear, editar, eliminar y buscar tareas escolares
- **Organización por materias**: Sistema integrado con materias predefinidas y personalizadas
- **Control de estados**: Marca tareas como pendientes o completadas
- **Fechas de entrega**: Seguimiento de fechas de inicio y entrega
- **Búsqueda avanzada**: Busca tareas por múltiples criterios (materia, descripción, fecha, estado)
- **Persistencia de datos**: Almacenamiento automático en formato JSON
- **Interfaz intuitiva**: Menú interactivo con emojis y visualización clara
- **Estadísticas**: Resumen y progreso de tareas completadas

## Requisitos 📋

- Python 3.6 o superior
- No requiere dependencias externas (usa solo bibliotecas estándar de Python)

## Instalación 🚀

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/gestor-tareas-colegio.git
cd gestor-tareas-colegio
```

2. (Opcional) Crea un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

## Uso 💻

Ejecuta el programa principal:

```bash
python main.py
```

### Menú Principal

El programa ofrece las siguientes opciones:

1. **Agregar tarea** - Crea una nueva tarea con todos sus detalles
2. **Ver detalle de tarea** - Muestra información completa de una tarea específica
3. **Ver todas las tareas** - Lista todas las tareas organizadas por estado
4. **Ver tareas pendientes** - Muestra solo las tareas no completadas
5. **Ver tareas completadas** - Muestra el historial de tareas finalizadas
6. **Buscar tarea** - Búsqueda por múltiples criterios
7. **Editar tarea** - Modifica cualquier campo de una tarea existente
8. **Eliminar tarea** - Borra una tarea específica
9. **Borrar todas las tareas** - Limpia completamente la base de datos (con confirmación)
10. **Salir** - Guarda y cierra el programa

## Estructura del Proyecto 📁

```
gestor-tareas-colegio/
│
├── main.py           # Punto de entrada de la aplicación
├── menu.py           # Sistema de menús e interacción con usuario
├── tareas.py         # Lógica de negocio para gestión de tareas
├── materias.py       # Gestión del catálogo de materias
├── archivo.py        # Persistencia y manejo de archivos JSON
├── vistas.py         # Presentación y formateo de información
├── utils.py          # Utilidades generales del sistema
└── tareas.json       # Base de datos local (generado automáticamente)
```

## Arquitectura 🏗️

La aplicación sigue una arquitectura modular con separación de responsabilidades:

### Módulos Principales

- **main.py**: Punto de entrada y coordinación general
- **menu.py**: Capa de presentación (interfaz de usuario)
- **tareas.py**: Capa de lógica de negocio
- **archivo.py**: Capa de persistencia de datos
- **vistas.py**: Formateo y visualización de datos
- **materias.py**: Gestión del catálogo de materias
- **utils.py**: Funciones auxiliares compartidas

### Flujo de Datos

1. El usuario interactúa a través del menú (menu.py)
2. Las operaciones se ejecutan en la lógica de negocio (tareas.py)
3. Los datos se persisten automáticamente (archivo.py)
4. La información se presenta formateada (vistas.py)

## Características Técnicas 🔧

- **Persistencia automática**: Los datos se guardan automáticamente al salir
- **Manejo de errores**: Validación robusta de entrada de usuario
- **Código documentado**: Docstrings y comentarios explicativos
- **Sin dependencias**: Usa solo bibliotecas estándar de Python
- **Multiplataforma**: Funciona en Windows, macOS y Linux
- **Recuperación ante fallos**: Guarda datos incluso en salidas abruptas (Ctrl+C)

## Materias Disponibles 📖

El sistema incluye las siguientes materias predefinidas:
- Matemáticas
- Lengua
- Historia
- Geografía
- Ciencias Naturales
- Inglés
- Educación Física
- Arte
- Música
- Informática
- Física
- Química
- Biología
- Opción para agregar materias personalizadas

## Formato de Datos 💾

Las tareas se almacenan en formato JSON con la siguiente estructura:

```json
{
  "1": {
    "materia": "Matemáticas",
    "descripcion": "Resolver ejercicios del capítulo 5",
    "fecha_inicio": "2024-01-15",
    "fecha_fin": "2024-01-20",
    "completada": false,
    "codigo": "T-0001",
    "observaciones": "Páginas 45-50"
  }
}
```

## Contribuciones 🤝

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia 📄

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor ✒️

Desarrollado con dedicación para ayudar a estudiantes a organizar mejor sus tareas escolares.

---

*¡Organiza tus tareas y mejora tu rendimiento académico!* 🎯