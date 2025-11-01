"""
GESTOR DE MATERIAS ESCOLARES

UTILIDAD:
Este archivo contiene toda la lógica relacionada con las materias escolares.
Incluye el catálogo base, funciones de selección y visualización, y todas las
operaciones de gestión (crear, leer, actualizar, eliminar).

DEPENDENCIAS:
- utils.py: Proporciona funciones de interfaz (limpiar_pantalla, pausar, linea_separadora)

¿POR QUÉ ESTA DEPENDENCIA?
- utils.py centraliza las funciones de interfaz para consistencia en todo el sistema
"""

# Importa funciones de interfaz
from utils import limpiar_pantalla, pausar, linea_separadora

# ============================================
# CATÁLOGO BASE DE MATERIAS
# ============================================

# Diccionario con las materias escolares más comunes
# La clave es un número para facilitar la selección
# El valor es el nombre de la materia
MATERIAS = {
    1: "Matematicas",
    2: "Lengua",
    3: "Historia",
    4: "Geografia",
    5: "Ciencias Naturales",
    6: "Ingles",
    7: "Educacion Fisica",
    8: "Arte",
    9: "Musica",
    10: "Informatica",
    11: "Fisica",
    12: "Quimica",
    13: "Biologia"
}

# ============================================
# FUNCIONES DE VISUALIZACIÓN Y SELECCIÓN
# ============================================

def mostrar_materias():
    """Muestra la lista numerada de materias"""
    # Imprime el título de la lista
    print("\nMATERIAS DISPONIBLES:")
    # Dibuja una línea decorativa de 30 caracteres con guiones
    linea_separadora(30, "-")
    # Itera sobre el diccionario de materias
    for num, materia in MATERIAS.items():
        # Imprime cada materia con su número (formato de 2 dígitos)
        print(f"{num:2}. {materia}")
    # Agrega la opción de materia personalizada al final
    # El número es el total de materias + 1
    print(f"{len(MATERIAS) + 1:2}. Otra materia (personalizada)")
    # Dibuja línea decorativa inferior
    linea_separadora(30, "-")

def seleccionar_materia():
    """Permite al usuario seleccionar una materia"""
    # Primero muestra la lista de materias disponibles
    mostrar_materias()

    # Bucle infinito hasta que el usuario seleccione una opción válida
    while True:
        try:
            # Solicita al usuario que ingrese un número
            opcion = input("\nSeleccione materia (numero): ").strip()
            # Convierte el texto a número entero
            num = int(opcion)

            # Verifica si el número corresponde a una materia predefinida
            if num in MATERIAS:
                # Retorna el nombre de la materia seleccionada
                return MATERIAS[num]

            # Verifica si eligió la opción de materia personalizada
            elif num == len(MATERIAS) + 1:
                # Pide al usuario que ingrese el nombre de la materia
                materia_custom = input("Nombre de la materia: ").strip()
                # Valida que tenga al menos 2 caracteres
                if materia_custom and len(materia_custom) >= 2:
                    # Retorna el nombre personalizado
                    return materia_custom
                else:
                    # Muestra error si el nombre es muy corto
                    print("El nombre debe tener al menos 2 caracteres")
            else:
                # El número no está en el rango válido
                print("Numero invalido")

        except ValueError:
            # Captura el error si el usuario no ingresó un número
            print("Por favor ingrese un numero")
        except KeyboardInterrupt:
            # Captura Ctrl+C para cancelar la selección
            print("\nOperacion cancelada")
            # Retorna None indicando que se canceló
            return None

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