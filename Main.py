import os
from manejo_de_usuario import (
    pedir_nombre_usuario,
    mostrar_estadisticas_usuario,
    mostrar_ranking_usuarios
)
from procesos_recopilatorios import jugar_partida_y_guardar_estadisticas_nueva
from Minijuego import jugar_guardianes
import os

def main():
    BASE_DIR = os.path.dirname(__file__)
    USUARIOS_FILE = os.path.join(BASE_DIR, "Usuarios.json")
    PREGUNTAS_FILE = os.path.join(BASE_DIR, "Preguntas.csv")
    BASE_DIR_MAIN = os.path.dirname(os.path.abspath(__file__))
    print("¡Bienvenid@ soldado! ¿Listo para la batalla?")
    print("=" * 50)
    nombre = pedir_nombre_usuario()
    
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Juego principal")
        print("2. Ver mis estadísticas")
        print("3. Ver ranking")
        print("4. Mini juego extra")
        print("5. Salir")

        opcion = input("Selecciona una opción (1-5): ").strip()

        match opcion:
            case "1":
                jugar_partida_y_guardar_estadisticas_nueva(nombre, USUARIOS_FILE, PREGUNTAS_FILE)
            case "2":
                mostrar_estadisticas_usuario(nombre, USUARIOS_FILE)
            case "3":
                mostrar_ranking_usuarios(USUARIOS_FILE)
            case "4":
                jugar_guardianes()
            case "5":
                print("👋 ¡Gracias por jugar! ¡Hasta la próxima!")
                break
            case _:
                print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()


