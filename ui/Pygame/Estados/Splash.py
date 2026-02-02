import pygame
from .base import BaseEstado

class slpash(BaseEstado):
    def __init__(self, parametros):
        super(slpash, self).__init__()
        self.title = self.font.render("Incompetent Game", True, pygame.Color("blue"))
        self.titulo_rect = self.titulo.get_rect(center=self.screen_rect.center)
        self.sig_estado = "MENU"
        self.tiempo_activo = 0
    
    def update(self, dt):
        self.tiempo_activo += dt
        if self.tiempo_activo >= 5000:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
