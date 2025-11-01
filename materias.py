"""
MÓDULO DE MATERIAS - Catálogo Base
Catálogo de materias escolares disponibles

UTILIDAD:
Este archivo contiene el catálogo base de materias escolares y las funciones
básicas de visualización y selección. Proporciona una lista predefinida de
asignaturas comunes y permite al usuario seleccionar una de ellas o ingresar
una materia personalizada.

DEPENDENCIAS:
- utils.py: Necesita linea_separadora() para dibujar líneas decorativas en el menú

¿POR QUÉ ESTA DEPENDENCIA?
- utils.py centraliza todas las funciones de formato visual
- La gestión avanzada del catálogo está en gestor_materias.py
"""

# Importa la función para dibujar líneas decorativas
from utils import linea_separadora

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