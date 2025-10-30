# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python console application for managing school homework tasks. The system uses a modular architecture with clear separation of concerns between presentation, business logic, and data persistence layers.

## Common Development Commands

### Running the Application
```bash
python main.py
# or
python3 main.py
```

### Virtual Environment Setup (if needed)
```bash
# Create virtual environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### Testing Individual Modules
```bash
# Test specific functionality
python -c "import tareas; print(tareas.obtener_tareas())"

# Interactive testing
python -i tareas.py  # Opens interactive shell with module loaded
```

## High-Level Architecture

### Core Data Flow
1. **Entry Point**: `main.py` orchestrates the application lifecycle
2. **User Interface**: `menu.py` handles all user interaction and input validation
3. **Business Logic**: `tareas.py` manages task CRUD operations and state
4. **Persistence**: `archivo.py` handles JSON serialization/deserialization
5. **Presentation**: `vistas.py` formats and displays data to the user
6. **Utilities**: `utils.py` provides cross-cutting concerns (formatting, validation)
7. **Domain**: `materias.py` manages subject catalog and selection

### Key Architectural Patterns

#### Global State Management
- **tareas_colegio** dictionary in `tareas.py` acts as the in-memory database
- **siguiente_id** counter ensures unique task IDs with auto-increment
- State modifications use the `global` keyword when necessary

#### ID and Code System
- Tasks have both numeric IDs (internal) and formatted codes (T-XXXX format)
- Codes are generated from IDs: `generar_codigo_tarea(id_tarea)`
- After loading from JSON, codes are synchronized: `sincronizar_codigos_con_ids()`

#### Data Schema Evolution
- The system handles legacy `fecha_entrega` field by mapping it to `fecha_fin`
- `_normalizar_tarea_dict()` in archivo.py ensures backward compatibility
- JSON structure supports both dict-based and list-based formats

#### Menu Flow Control
- `ejecutar_menu_principal()` implements the main event loop
- Each menu option returns a boolean to control continuation
- Option "10" (exit) returns False to break the loop
- All other operations preserve state and return to menu

### Critical Implementation Details

#### Task Structure
Each task contains these fields:
- **materia**: Subject name (string)
- **descripcion**: Task description (string)
- **fecha_inicio**: Start date (optional string)
- **fecha_fin**: Due date (required string, was fecha_entrega in legacy)
- **completada**: Completion status (boolean)
- **codigo**: Auto-generated code (T-XXXX format)
- **observaciones**: Additional notes (optional string)

#### Subject System
- 13 predefined subjects plus "Otra" (custom) option
- Dual identification: by number (1-14) or code (MAT, LEN, etc.)
- `seleccionar_materia()` accepts both input formats
- Custom subjects prompt for user-defined names

#### File Persistence Strategy
- JSON is the sole persistence format (tareas.txt support removed)
- Auto-save occurs on:
  - Normal exit
  - Keyboard interrupt (Ctrl+C)
  - After critical operations (add, edit, delete)
- File structure: `{"version": 1, "tareas": {id: task_dict}}`

#### Error Handling Hierarchy
1. Try normal execution
2. Catch KeyboardInterrupt → save and exit gracefully
3. Catch generic exceptions → attempt save before crash
4. Context managers ensure file handles are closed

#### View Rendering Patterns
- `vistas.py` never modifies data, only displays it
- Statistics are calculated on-demand via `obtener_estadisticas()`
- Progress bars use Unicode characters: █ (filled) and ░ (empty)
- Grouping by subject uses dictionary comprehension

## Important Behaviors

### ID Management
- IDs start at 1 and increment monotonically
- After loading tasks, siguiente_id = max(existing_ids) + 1
- Deleted IDs are not reused
- Empty task list resets siguiente_id to 1

### Search Functionality
- Searches by exact ID match first
- Then searches in materia and descripcion (case-insensitive)
- Returns all matches, not just the first one

### Task Completion
- One-way operation (cannot un-complete via marcar_completada)
- Edit function allows toggling completion status
- Completed tasks remain in the system until explicitly deleted

### Data Validation
- Descriptions and due dates are required
- Subject names must have at least 2 characters
- IDs must be valid integers for operations
- Empty inputs are rejected with error messages

### Screen Management
- `limpiar_pantalla()` uses platform-specific commands (cls/clear)
- `pausar()` waits for Enter key after operations
- Menu redraws completely after each operation

## Testing Scenarios

### Common Test Cases
1. **First Run**: No tareas.json exists → creates on first save
2. **Empty State**: All operations handle empty task list gracefully
3. **ID Boundaries**: Test with ID 1, max_int, and invalid IDs
4. **Unicode Handling**: Emojis and special characters in descriptions
5. **Legacy Migration**: Old fecha_entrega fields map to fecha_fin

### Edge Cases to Consider
- Simultaneous operations (not thread-safe)
- Very long descriptions (truncated in list views)
- Invalid JSON in tareas.json (error message, empty start)
- File permissions issues (catches PermissionError)
- Circular imports (avoided through careful module design)

## Code Maintenance Notes

### Module Dependencies
```
main.py → menu, archivo, utils
menu.py → tareas, materias, archivo, vistas, utils
tareas.py → (no imports, self-contained)
archivo.py → tareas, json, os
vistas.py → tareas
materias.py → (no imports, self-contained)
utils.py → tareas, os, sys
```

### Function Naming Conventions
- `obtener_*`: Getter functions that return data
- `mostrar_*`: Display functions that print to console
- `opcion_*`: Menu option handlers
- `validar_*`: Validation functions returning bool
- Private functions start with `_` (e.g., `_normalizar_tarea_dict`)

### Global State Access Points
- Read tasks: `tareas.obtener_tareas()`
- Modify tasks: Direct dictionary access in tareas.py only
- Set all tasks: `tareas.establecer_tareas(dict)`
- Next ID: Internal to tareas.py, not exposed

### Critical Synchronization Points
1. After loading from JSON: `sincronizar_codigos_con_ids()`
2. After adding task: ID counter increments
3. After deleting all: Reset siguiente_id to 1
4. Before saving: Normalize all task data

## Performance Considerations

- Dictionary lookups are O(1) for task access by ID
- No pagination for large task lists (could be issue with 1000+ tasks)
- Statistics calculation iterates all tasks each time (not cached)
- File I/O occurs synchronously (blocks UI)
- No background saving or auto-save timer