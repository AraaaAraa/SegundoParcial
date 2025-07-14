import pygame, random
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Minijuego import generar_matriz_resoluble, obtener_valores_vecinos_no_nulos
from utilidades_pygame import pantalla, colores, fuentes, dibujar_texto, esperar_click, dibujar_boton, dibujar_casilla_minijuego, usuario_minijuego, guardian_1, guardian_2, soldado_base, cueva

TAM = 5
TAM_CASILLA = 100
MARGEN = 10
ORIGEN_X = 100
ORIGEN_Y = 100

def dibujar_matriz(matriz, jugador_pos, camino):
    pantalla.blit(cueva, (0,0))
    
    i = 0
    while i < TAM:
        j = 0
        while j < TAM:
            x = ORIGEN_X + j * (TAM_CASILLA + MARGEN)
            y = ORIGEN_Y + i * (TAM_CASILLA + MARGEN)
            
            valor = matriz[i][j]
            
            color = colores['blanco']
            imagen_soldado = guardian_1  # Imagen por defecto
            
            # Verificar si está en el camino
            k = 0
            while k < len(camino):
                pos = camino[k]
                if pos[0] == i and pos[1] == j:
                    color = colores["azul"]
                    imagen_soldado = guardian_2  # Soldado diferente para camino recorrido
                    break
                k += 1

            # Color y imagen para la posición actual del jugador
            if jugador_pos[0] == i and jugador_pos[1] == j:
                color = colores["verde"]
                imagen_soldado = usuario_minijuego  # Imagen del jugador
            
            # Usar la nueva función para dibujar casillas con imágenes
            dibujar_casilla_minijuego(x, y, str(valor), color, colores["blanco"], fuentes["chica"], imagen_soldado, TAM_CASILLA)
            
            j += 1
        i += 1

def mostrar_instrucciones() -> pygame.Rect:
    x = 775
    y = 120
    lineas = [
        "🧭 Instrucciones:",
        "• Llegá a la esquina inferior",
        "  derecha desde la superior izquierda.",
        "• Solo podés moverte a casillas",
        "  con valores mayores al actual.",
        "• Hacé clic sobre casillas válidas.",
        "",
        "🎮 Soldado con tinte verde = tu posición",
        "⚔️ Soldado con tinte azul = camino recorrido",
        "🛡️ Soldado normal = casillas disponibles"
    ]
    i = 0
    while i < len(lineas):
        dibujar_texto(lineas[i], fuentes['chica'], colores['blanco'], x, y)
        y += 30
        i += 1

    return dibujar_texto("Volver al menú", fuentes['chica'], colores['rojo'], x, y + 20)

def obtener_movimientos_validos(matriz, jugador_pos, valor_actual):
    fila = jugador_pos[0]
    col = jugador_pos[1]
    direcciones = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    movimientos = []

    d = 0
    while d < len(direcciones):
        df = direcciones[d][0]
        dc = direcciones[d][1]
        nueva_fila = fila + df
        nueva_col = col + dc

        if nueva_fila >= 0 and nueva_fila < TAM and nueva_col >= 0 and nueva_col < TAM:
            nuevo_valor = matriz[nueva_fila][nueva_col]
            if nuevo_valor > valor_actual:
                movimientos.append((nueva_fila, nueva_col))
        d += 1

    return movimientos

def casilla_clickeada(pos_mouse):
    i = 0
    while i < TAM:
        j = 0
        while j < TAM:
            x = ORIGEN_X + j * (TAM_CASILLA + MARGEN)
            y = ORIGEN_Y + i * (TAM_CASILLA + MARGEN)
            rect = pygame.Rect(x, y, TAM_CASILLA, TAM_CASILLA)
            if rect.collidepoint(pos_mouse):
                return (i, j)
            j += 1
        i += 1
    return None

def mostrar_mensaje_final(texto):
    pantalla.blit(cueva, (0,0))
    dibujar_texto(texto, fuentes['grande'], colores['blanco'], 450, 300)
    boton = dibujar_texto("Volver al menú", fuentes['chica'], colores['rojo'], 450, 400)
    pygame.display.flip()
    esperar_click([boton])

def jugar_guardianes_pygame():
    matriz = generar_matriz_resoluble(TAM)
    jugador_pos = (0, 0)
    camino = []
    objetivo = (TAM - 1, TAM - 1)
    valor_actual = matriz[0][0]

    while True:
        movimientos_validos = obtener_movimientos_validos(matriz, jugador_pos, valor_actual)

        if jugador_pos[0] == objetivo[0] and jugador_pos[1] == objetivo[1]:
            mostrar_mensaje_final("🎉 ¡GANASTE!")
            return

        if len(movimientos_validos) == 0:
            mostrar_mensaje_final("❌ ¡PERDISTE!")
            return

        dibujar_matriz(matriz, jugador_pos, camino)
        boton_volver = mostrar_instrucciones()
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volver.collidepoint(evento.pos):
                    return

                clic = casilla_clickeada(evento.pos)
                if clic is not None:
                    m = 0
                    while m < len(movimientos_validos):
                        mov = movimientos_validos[m]
                        if mov[0] == clic[0] and mov[1] == clic[1]:
                            camino.append(jugador_pos)
                            jugador_pos = mov
                            valor_actual = matriz[mov[0]][mov[1]]
                            break
                        m += 1
        pygame.time.Clock().tick(60)