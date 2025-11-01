"""
GESTOR DE MATERIAS ESCOLARES

UTILIDAD:
Este archivo contiene toda la lógica de gestión del catálogo de materias.
Maneja las operaciones CRUD (crear, leer, actualizar, eliminar) sobre el
catálogo de materias y proporciona el submenú de gestión.

DEPENDENCIAS:
- materias.py: Accede y modifica el diccionario MATERIAS que contiene el catálogo
- utils.py: Proporciona funciones de interfaz (limpiar_pantalla, pausar, linea_separadora)

¿POR QUÉ ESTAS DEPENDENCIAS?
- materias.py contiene el catálogo base y las funciones de visualización
- utils.py centraliza las funciones de interfaz para consistencia
"""

# Importa el catálogo de materias y funciones de visualización
from materias import MATERIAS, mostrar_materias

# Importa funciones de interfaz
from utils import limpiar_pantalla, pausar, linea_separadora

# ============================================
# FUNCIONES DE GESTIÓN DE MATERIAS
# ============================================

def obtener_siguiente_numero():
    """Obtiene el siguiente número disponible para una nueva materia"""
    # Si no hay materias, empezar desde 1
    if not MATERIAS:
        return 1
    # Obtener el número más alto y sumar 1
    return max(MATERIAS.keys()) + 1

def agregar_materia():
    """Agrega una nueva materia al catálogo"""
    # Muestra las materias actuales
    mostrar_materias()

    # Solicita el nombre de la nueva materia
    print("\nAGREGAR NUEVA MATERIA")
    nombre = input("Nombre de la materia: ").strip()

    # Valida que no esté vacío y tenga al menos 2 caracteres
    if not nombre or len(nombre) < 2:
        print("El nombre debe tener al menos 2 caracteres")
        return False

    # Verifica que no exista ya
    if nombre in MATERIAS.values():
        print(f"La materia '{nombre}' ya existe en el catalogo")
        return False

    # Obtiene el siguiente número disponible
    nuevo_numero = obtener_siguiente_numero()

    # Agrega la materia al diccionario
    MATERIAS[nuevo_numero] = nombre

    print(f"\nMateria '{nombre}' agregada con el numero {nuevo_numero}")
    return True

def editar_materia():
    """Edita el nombre de una materia existente"""
    # Muestra las materias actuales
    mostrar_materias()

    # Si no hay materias, no hay nada que editar
    if not MATERIAS:
        print("\nNo hay materias para editar")
        return False

    try:
        # Solicita el número de la materia a editar
        num = int(input("\nNumero de la materia a editar: ").strip())

        # Verifica que el número exista
        if num not in MATERIAS:
            print("Numero de materia invalido")
            return False

        # Muestra la materia actual
        print(f"Materia actual: {MATERIAS[num]}")

        # Solicita el nuevo nombre
        nuevo_nombre = input("Nuevo nombre (ENTER para cancelar): ").strip()

        # Si está vacío, cancela
        if not nuevo_nombre:
            print("Operacion cancelada")
            return False

        # Valida longitud mínima
        if len(nuevo_nombre) < 2:
            print("El nombre debe tener al menos 2 caracteres")
            return False

        # Actualiza el nombre
        nombre_anterior = MATERIAS[num]
        MATERIAS[num] = nuevo_nombre

        print(f"\nMateria '{nombre_anterior}' cambiada a '{nuevo_nombre}'")
        return True

    except ValueError:
        print("Por favor ingrese un numero valido")
        return False

def eliminar_materia():
    """Elimina una materia del catálogo"""
    # Muestra las materias actuales
    mostrar_materias()

    # Si no hay materias, no hay nada que eliminar
    if not MATERIAS:
        print("\nNo hay materias para eliminar")
        return False

    try:
        # Solicita el número de la materia a eliminar
        num = int(input("\nNumero de la materia a eliminar: ").strip())

        # Verifica que el número exista
        if num not in MATERIAS:
            print("Numero de materia invalido")
            return False

        # Muestra la materia que se va a eliminar
        materia_eliminar = MATERIAS[num]
        print(f"Se eliminara: {materia_eliminar}")

        # Pide confirmación
        confirmar = input("Esta seguro? (S/N): ").upper()

        if confirmar == "S":
            # Elimina la materia
            del MATERIAS[num]
            print(f"\nMateria '{materia_eliminar}' eliminada")

            # Reorganiza los números si es necesario
            reorganizar_numeros()
            return True
        else:
            print("Operacion cancelada")
            return False

    except ValueError:
        print("Por favor ingrese un numero valido")
        return False

def reorganizar_numeros():
    """Reorganiza los números de las materias para que sean consecutivos"""
    # Si no hay materias o solo hay una, no hay nada que reorganizar
    if len(MATERIAS) <= 1:
        return

    # Crea una lista temporal con los valores actuales
    materias_temp = list(MATERIAS.values())

    # Limpia el diccionario
    MATERIAS.clear()

    # Reasigna con números consecutivos
    for i, materia in enumerate(materias_temp, 1):
        MATERIAS[i] = materia

def mostrar_catalogo_completo():
    """Muestra todas las materias sin la opción personalizada"""
    # Limpia la pantalla
    limpiar_pantalla()
    linea_separadora()
    print("         CATALOGO DE MATERIAS")
    linea_separadora()

    if not MATERIAS:
        print("\nNo hay materias en el catalogo")
        print("Use la opcion 'Agregar materia' para comenzar")
    else:
        print("\nMaterias disponibles:")
        linea_separadora(40, "-")
        for num, materia in sorted(MATERIAS.items()):
            print(f"  {num:2}. {materia}")
        linea_separadora(40, "-")
        print(f"\nTotal: {len(MATERIAS)} materia(s)")

# ============================================
# SUBMENÚ DE GESTIÓN
# ============================================

def submenu_gestionar_materias():
    """Submenú para gestionar el catálogo de materias"""
    opciones = {
        "1": ("Ver catalogo completo", mostrar_catalogo_completo),
        "2": ("Agregar materia", agregar_materia),
        "3": ("Editar materia", editar_materia),
        "4": ("Eliminar materia", eliminar_materia),
        "5": ("Volver al menu principal", None),
    }

    while True:
        # Limpia la pantalla y muestra el menú
        limpiar_pantalla()
        linea_separadora()
        print("         GESTIONAR MATERIAS - SUBMENU")
        linea_separadora()

        # Muestra las opciones
        for num, (descripcion, _) in opciones.items():
            print(f"{num}. {descripcion}")

        linea_separadora()

        # Solicita la opción
        opcion = input("\nSeleccione una opcion (1-5): ").strip()

        # Si es volver, sale del bucle
        if opcion == "5":
            break

        # Ejecuta la opción seleccionada
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