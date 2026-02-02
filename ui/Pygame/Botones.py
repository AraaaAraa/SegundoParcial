import pygame


class Boton:
    def __init__(self, texto, x, y, ancho, alto, fuente, color_fondo='gray'):
        self.texto = texto
        self.fuente = fuente
        # Creamos el rectángulo del botón correctamente con su posición y tamaño
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_fondo = color_fondo
        
    def draw(self, superficie):
        # 1. Dibujamos el rectángulo del botón en la superficie que recibimos
        pygame.draw.rect(superficie, self.color_fondo, self.rect, 0, 5)
        
        # 2. Renderizamos el texto usando la fuente que le pasamos al constructor
        texto_render = self.fuente.render(self.texto, True, 'black')
        
        # 3. Calculamos el centro para que el texto quede perfecto
        texto_rect = texto_render.get_rect(center=self.rect.center)
        
        # 4. Dibujamos el texto sobre la superficie
        superficie.blit(texto_render, texto_rect)

    def verificar_click(self, pos_mouse):
        # Método útil para saber si el usuario tocó el botón
        return self.rect.collidepoint(pos_mouse)