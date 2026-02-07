# =============================================================================
# ESTADO MENU
# =============================================================================
# Pantalla del menú principal del juego
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto


class menu(BaseEstado):
    """
    Estado del menú principal.
    
    Ofrece opciones para:
    - Jugar
    - Ver Historia
    - Salir
    """
    
    def __init__(self):
        """Inicializa el estado del menú."""
        super(menu, self).__init__()
        self.sig_estado = "Gameplay"
        
        # Colores
        self.color_fondo_1 = (20, 20, 50)
        self.color_fondo_2 = (50, 20, 70)
        self.color_titulo = (255, 215, 0)
        self.color_sombra = (50, 50, 50)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_boton = pygame.font.Font(None, 40)
        
        # Título
        self.titulo = "TRIVIA MITOLÓGICA"
        
        # Botones
        centro_x = self.screen_rect.centerx
        self.boton_jugar = Boton(
            "Jugar", 
            centro_x - 150, 
            250, 
            300, 
            60, 
            self.fuente_boton,
            (100, 200, 100)
        )
        self.boton_historia = Boton(
            "Historia", 
            centro_x - 150, 
            330, 
            300, 
            60, 
            self.fuente_boton,
            (100, 100, 200)
        )
        self.boton_salir = Boton(
            "Salir", 
            centro_x - 150, 
            410, 
            300, 
            60, 
            self.fuente_boton,
            (200, 100, 100)
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
            if self.boton_jugar.verificar_click(pos):
                self.sig_estado = "Gameplay"
                self.done = True
            elif self.boton_historia.verificar_click(pos):
                self.sig_estado = "Historia"
                self.done = True
            elif self.boton_salir.verificar_click(pos):
                self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
    
    def update(self, dt: float):
        """
        Actualiza el estado del menú.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        pass
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el menú en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Fondo con degradado
        dibujar_degradado_vertical(surface, self.color_fondo_1, self.color_fondo_2)
        
        # Título con sombra
        pos_titulo = (self.screen_rect.centerx, 120)
        dibujar_sombra_texto(
            surface, 
            self.titulo, 
            self.fuente_titulo,
            self.color_titulo,
            self.color_sombra,
            pos_titulo,
            offset=4
        )
        
        # Botones
        self.boton_jugar.draw(surface)
        self.boton_historia.draw(surface)
        self.boton_salir.draw(surface)
