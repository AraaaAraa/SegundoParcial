from interfaz_pygame import mostrar_pantalla_bienvenida, mostrar_pantalla_ingreso_nombre, ejecutar_menu_principal

import pygame


def main():
    """
    Punto de entrada del juego. Inicializa la interfaz y lanza el menú principal.
    """
    pygame.init()
    mostrar_pantalla_bienvenida()
    nombre_usuario = mostrar_pantalla_ingreso_nombre()
    ejecutar_menu_principal(nombre_usuario)


if __name__ == "__main__":
    main()