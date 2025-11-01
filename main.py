"""
GESTOR DE TAREAS DEL COLEGIO - Punto de entrada
"""

from gestor_tareas import ejecutar_menu_principal
from utils import mostrar_despedida

def main():
    """Función principal del programa"""
    try:
        ejecutar_menu_principal()
        mostrar_despedida()

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
        print("Hasta luego!")

    except Exception as error:
        print(f"\nError inesperado: {error}")

if __name__ == "__main__":
    main()