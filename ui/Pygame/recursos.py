# =============================================================================
# MÓDULO DE RECURSOS
# =============================================================================
# Maneja la carga de recursos (fuentes e imágenes) para Pygame
# =============================================================================

import pygame
import os

# Rutas base
BASE_DIR = os.path.dirname(__file__)
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")


def cargar_fuente(nombre: str, tamaño: int) -> pygame.font.Font:
    """
    Carga una fuente desde el directorio de fuentes.
    
    Parámetros:
        nombre (str): Nombre del archivo de fuente
        tamaño (int): Tamaño de la fuente
    
    Retorna:
        pygame.font.Font: Fuente cargada o fuente por defecto si no existe
    """
    ruta = os.path.join(FONTS_DIR, nombre)
    if os.path.exists(ruta):
        return pygame.font.Font(ruta, tamaño)
    else:
        return pygame.font.Font(None, tamaño)


def cargar_imagen(nombre: str) -> pygame.Surface:
    """
    Carga una imagen desde el directorio de imágenes.
    
    Parámetros:
        nombre (str): Nombre del archivo de imagen
    
    Retorna:
        pygame.Surface: Imagen cargada o superficie magenta si no existe
    """
    ruta = os.path.join(IMAGES_DIR, nombre)
    if os.path.exists(ruta):
        return pygame.image.load(ruta).convert_alpha()
    else:
        # Crear superficie de placeholder magenta si no existe la imagen
        img = pygame.Surface((100, 100))
        img.fill((255, 0, 255))
        return img
