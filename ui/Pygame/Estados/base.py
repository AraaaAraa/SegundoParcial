import pygame

class BaseEstado(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.sig_estado = None
        self.pantalla_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

    def startup(self, persit):
        self.persi = persit

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass