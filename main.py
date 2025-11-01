"""
GESTOR DE TAREAS DEL COLEGIO - Punto de entrada
Sistema simplificado sin persistencia
"""

from gestor_tareas import ejecutar_menu_principal, obtener_estadisticas
from utils import mostrar_despedida

def main():
    """Función principal del programa"""
    try:
        ejecutar_menu_principal()
        stats = obtener_estadisticas()
        mostrar_despedida(stats)

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
        print("Hasta luego!")

    except Exception as error:
        print(f"\nError inesperado: {error}")

if __name__ == "__main__":
    main()