"""
GESTOR DE TAREAS DEL COLEGIO - Punto de entrada

UTILIDAD:
Este archivo es el punto de entrada del programa. Su única responsabilidad es
iniciar el sistema, manejar errores generales y mostrar el mensaje de despedida.
Es el archivo que se ejecuta directamente: python main.py

DEPENDENCIAS:
- gestor_tareas.py: Necesita ejecutar_menu_principal() que contiene toda la
  lógica del programa y el sistema de menús
- herramientas.py: Necesita mostrar_despedida() para mostrar el mensaje final al salir

¿POR QUÉ ESTAS DEPENDENCIAS?
- gestor_tareas.py maneja toda la lógica, por eso main.py solo lo llama
- herramientas.py tiene la función de despedida para mantener main.py simple
"""

# Importa la función principal que ejecuta todo el sistema de menús
# y la función para cargar tareas de ejemplo
from gestor_tareas import ejecutar_menu_principal, cargar_tareas_ejemplo
# Importa la función que muestra el mensaje de despedida
from herramientas import mostrar_despedida

def main():
    """Función principal del programa"""
    try:
        # Carga las tareas de ejemplo al iniciar
        # Como no hay persistencia, esto da contexto y demuestra funcionalidad
        cargar_tareas_ejemplo()

        # Ejecuta el menú principal (toda la lógica del programa)
        ejecutar_menu_principal()
        # Cuando el usuario sale normalmente (opción 9), muestra despedida
        mostrar_despedida()

    except KeyboardInterrupt:
        # Captura Ctrl+C para salir limpiamente
        print("\n\nPrograma interrumpido por el usuario")
        print("Hasta luego!")

    except Exception as error:
        # Captura cualquier otro error no esperado
        print(f"\nError inesperado: {error}")

# Este bloque solo se ejecuta si el archivo se ejecuta directamente
# No se ejecuta si el archivo es importado desde otro módulo
if __name__ == "__main__":
    # Llama a la función principal para iniciar el programa
    main()