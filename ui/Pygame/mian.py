import pygame
import sys
from Estados.Game_Over  import gameOver
from Estados.Menu import menu
from Estados.Gamepley import gameplay
from Estados.Historia import historia
from Estados.Splash import splash
from config.constantes import ANCHO, ALTO, FPS
from Juego import juego
# Initialize all imported pygame modules
pygame.init()

# Create the window surface
pantalla = pygame.display.set_mode((ANCHO, ALTO))
estados = {
    "Menu": menu(),
    "Gameplay": gameplay(),
    "Historia": historia(),
    "Gameover": gameOver(),
    "Splash": splash()
}
Juego = juego(pantalla, estados, "Splash", FPS)
Juego.run()

pygame.quit
sys.exit
