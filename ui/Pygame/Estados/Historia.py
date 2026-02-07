# =============================================================================
# ESTADO HISTORIA
# =============================================================================
# Pantalla que muestra la historia del juego
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical


class historia(BaseEstado):
    """
    Estado de la historia del juego.
    
    Muestra información sobre el juego y permite volver al menú.
    """
    
    def __init__(self):
        """Inicializa el estado de historia."""
        super(historia, self).__init__()
        self.sig_estado = "Menu"
        
        # Colores
        self.color_fondo_1 = (30, 20, 40)
        self.color_fondo_2 = (50, 30, 60)
        self.color_texto = (255, 255, 200)
        self.color_titulo = (255, 215, 0)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_texto = pygame.font.Font(None, 28)
        self.fuente_boton = pygame.font.Font(None, 40)
        
        # Texto de la historia
        self.lineas_historia = [
            "Bienvenido a la Trivia Mitológica",
            "",
            "En este juego pondrás a prueba tus conocimientos",
            "sobre mitología griega, romana y egipcia.",
            "",
            "Responde correctamente para acumular puntos",
            "y activa rachas para obtener buffeos especiales.",
            "",
            "¡Cuidado! Solo tienes 2 errores permitidos.",
            "",
            "¿Estás listo para el desafío?"
        ]
        
        # Botón volver
        centro_x = self.screen_rect.centerx
        self.boton_volver = Boton(
            "Volver",
            centro_x - 100,
            500,
            200,
            50,
            self.fuente_boton,
            (100, 100, 200)
        )
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.boton_volver.verificar_click(pos):
                self.done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.done = True
    
    def update(self, dt: float):
        """
        Actualiza el estado de historia.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        pass
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la historia en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Fondo con degradado
        dibujar_degradado_vertical(surface, self.color_fondo_1, self.color_fondo_2)
        
        # Título
        titulo_render = self.fuente_titulo.render("Historia", True, self.color_titulo)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 60))
        surface.blit(titulo_render, titulo_rect)
        
        # Líneas de historia
        y_offset = 150
        for linea in self.lineas_historia:
            texto_render = self.fuente_texto.render(linea, True, self.color_texto)
            texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(texto_render, texto_rect)
            y_offset += 35
        
        # Botón
        self.boton_volver.draw(surface)
