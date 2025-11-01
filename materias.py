"""
MÓDULO DE MATERIAS - Simplificado
Catálogo de materias escolares disponibles
"""

from utils import linea_separadora

# Diccionario de materias disponibles
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
    print("\nMATERIAS DISPONIBLES:")
    linea_separadora(30, "-")
    for num, materia in MATERIAS.items():
        print(f"{num:2}. {materia}")
    print(f"{len(MATERIAS) + 1:2}. Otra materia (personalizada)")
    linea_separadora(30, "-")

def seleccionar_materia():
    """Permite al usuario seleccionar una materia"""
    mostrar_materias()

    while True:
        try:
            opcion = input("\nSeleccione materia (numero): ").strip()
            num = int(opcion)

            # Opcion de materia predefinida
            if num in MATERIAS:
                return MATERIAS[num]

            # Opcion de materia personalizada
            elif num == len(MATERIAS) + 1:
                materia_custom = input("Nombre de la materia: ").strip()
                if materia_custom and len(materia_custom) >= 2:
                    return materia_custom
                else:
                    print("El nombre debe tener al menos 2 caracteres")
            else:
                print("Numero invalido")

        except ValueError:
            print("Por favor ingrese un numero")
        except KeyboardInterrupt:
            print("\nOperacion cancelada")
            return None