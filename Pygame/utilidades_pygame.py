import pygame
pygame.init()
# ============================
# 🎨 COLORES DEFINIDOS
# ============================
colores = {
    "blanco": (255, 255, 255),
    "negro": (0, 0, 0),
    "gris": (230, 230, 230),
    "azul": (50, 150, 255),
    "verde": (50, 200, 50),
    "rojo": (200, 50, 50)
}
# ============================
# 📐 TAMAÑO Y PANTALLA
# ============================
ANCHO, ALTO = 900, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Trivia Visual")
clock = pygame.time.Clock()

# ============================
# 🔠 FUENTES DEFINIDAS
# ============================
FUENTE_PATH = "Pygame/assets/oFuentes/Tangerine-Regular.ttf"
fuentes = {
    "grande": pygame.font.Font(FUENTE_PATH, 48),
    "mediana": pygame.font.Font(FUENTE_PATH, 32),
    "chica": pygame.font.Font(FUENTE_PATH, 27)
}

boton_normal = pygame.image.load("Pygame/assets/images/BotonNormal.png")
boton_oscuro = pygame.image.load("Pygame/assets/images/BotonOscuro.png")
fondo_desertico = pygame.image.load("Pygame/assets/images/FondoDesertico.png")
fondo_desertico = pygame.transform.scale(fondo_desertico, (ANCHO, ALTO))
soldado_base = pygame.image.load("Pygame/assets/images/SoldadoBase.png")
usuario_minijuego =  pygame.image.load("Pygame/assets/images/jugardor.png")
cueva = pygame.image.load("Pygame/assets/images/cueva.png")
cueva = pygame.transform.scale(cueva, (ANCHO, ALTO))
guardian_1 = pygame.image.load("Pygame/assets/images/soldado_1.png")
guardian_2 = pygame.image.load("Pygame/assets/images/soldado_2.png")

pared_estadisticas = pygame.image.load("Pygame/assets/images/pared_egipcia.webp")
pared_estadisticas = pygame.transform.scale(pared_estadisticas, (ANCHO, ALTO))
oscurecedor = pygame.Surface((ANCHO, ALTO))
oscurecedor.set_alpha(150)  # 0 (totalmente transparente) a 255 (opaco)
oscurecedor.fill((0, 0, 0))  # negro

# ============================
# ✏️ FUNCIONES AUXILIARES
# ============================
def dibujar_texto(texto: str, fuente: pygame.font.Font, color: tuple, x: int, y: int) -> pygame.Rect:
    """
    Dibuja un texto en la pantalla.

    Args:
        texto (str): Texto a mostrar.
        fuente (pygame.font.Font): Objeto fuente.
        color (tuple): Color del texto (RGB).
        x (int): Coordenada horizontal.
        y (int): Coordenada vertical.
        centrar (bool): Si debe centrarse o no.

    Returns:
        pygame.Rect: Rectángulo del texto renderizado.
    """
    renderizado = fuente.render(texto, True, color)
    rect = renderizado.get_rect(center=(x, y))
    texto = pantalla.blit(renderizado, rect)
    return texto


def esperar_click(botones: list[pygame.Rect]) -> int:
    """
    Espera un clic del usuario sobre alguno de los botones dados.

    Args:
        botones (list[pygame.Rect]): Lista de rectángulos interactivos.

    Returns:
        int: Índice del botón clickeado.
    """
    clic_realizado = False
    indice_clic = -1
    while not clic_realizado:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                indice = 0
                for boton in botones:
                    rect = boton
                    if rect.collidepoint(evento.pos):
                        indice_clic = indice
                        clic_realizado = True
                        break
                    indice += 1 
        pygame.time.Clock().tick(60) 

    return indice_clic


def dibujar_boton(x, y, texto, color_texto, fuente, imagen, ancho=350, alto=250):
    """
    Dibuja un botón con imagen de fondo y texto.
    
    Args:
        x, y: Posición del botón
        texto: Texto a mostrar
        color_texto: Color del texto
        fuente: Fuente del texto
        imagen: Imagen de fondo
        ancho, alto: Dimensiones del botón (opcional)
    
    Returns:
        pygame.Rect: Rectángulo del área clickeable
    """
    # Dibujar fondo (imagen escalada)
    imagen_escalada = pygame.transform.scale(imagen, (ancho, alto))
    pantalla.blit(imagen_escalada, (x, y))

    # Dibujar texto centrado
    botoncito = dibujar_texto(texto, fuente, color_texto, x + ancho//2, y + alto//2)

    return botoncito


def dibujar_casilla_minijuego(x, y, texto, color_fondo, color_texto, fuente, imagen_soldado, tamaño=100):
    """
    Dibuja una casilla específica para el minijuego usando imágenes de soldados.
    
    Args:
        x, y: Posición de la casilla
        texto: Texto a mostrar
        color_fondo: Color de fondo (usado para determinar el tinte)
        color_texto: Color del texto
        fuente: Fuente del texto
        imagen_soldado: Imagen del soldado a usar
        tamaño: Tamaño de la casilla
    
    Returns:
        pygame.Rect: Rectángulo del área clickeable
    """
    # Crear rectángulo para la casilla
    rect = pygame.Rect(x, y, tamaño, tamaño)
    
    # Escalar la imagen del soldado al tamaño de la casilla
    tamaño_soldado = int(tamaño * 2.3)
    imagen_escalada = pygame.transform.scale(imagen_soldado, (tamaño_soldado, tamaño_soldado))
    
    # Aplicar tinte de color según el estado
    if color_fondo == colores['verde']:  # Posición actual del jugador
        # Crear una superficie con tinte verde
        tinte = pygame.Surface((tamaño, tamaño))
        tinte.set_alpha(100)
        tinte.fill(colores['verde'])
        imagen_escalada.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    elif color_fondo == colores['azul']:  # Camino recorrido
        # Crear una superficie con tinte azul
        tinte = pygame.Surface((tamaño, tamaño))
        tinte.set_alpha(100)
        tinte.fill(colores['azul'])
        imagen_escalada.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    
    # Dibujar la imagen del soldado
    offset_x = (tamaño - tamaño_soldado) // 2
    offset_y = (tamaño - tamaño_soldado) // 2
    pantalla.blit(imagen_escalada, (x + offset_x, y + offset_y))
    
    # Dibujar borde negro para mayor visibilidad
    pygame.draw.rect(pantalla, colores['negro'], rect, 2)
    
    # Dibujar texto centrado sobre la imagen
    dibujar_texto(texto, fuente, color_texto, x + tamaño//2, y + tamaño//2)
    
    return rect