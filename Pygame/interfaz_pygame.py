import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilidades_pygame import dibujar_texto, esperar_click, colores, fuentes, pantalla, clock, fondo_desertico, oscurecedor, dibujar_boton, boton_normal, cueva, pared_estadisticas
from controlador_juego import iniciar_trivia, mostrar_resumen_final
from manejo_de_usuario import calcular_estadisticas, obtener_datos_ranking, ordenar_ranking
from minijuego_pygame import jugar_guardianes_pygame


def mostrar_pantalla_bienvenida() -> None:
    """
    Muestra la pantalla inicial de bienvenida hasta que el jugador haga clic.
    """
    continuar = False
    while not continuar:
        pantalla.blit(fondo_desertico, (0, 0))
        pantalla.blit(oscurecedor, (0, 0))
        dibujar_texto("🧠 TRIVIA VISUAL 🧠", fuentes['grande'], colores['blanco'], 450, 300)
        # x = 280 y = 275 boton
        boton = dibujar_boton(280,275, "Haz click para continuar", colores["blanco"], fuentes["mediana"], boton_normal)
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton.collidepoint(evento.pos):
                    continuar = True
        clock.tick(60)


def mostrar_pantalla_ingreso_nombre() -> str:
    """
    Muestra una pantalla donde el usuario puede ingresar su nombre.

    Returns:
        str: Nombre ingresado, validado.
    """
    nombre = ""
    escribiendo = True
    nombre_final = ""

    while escribiendo:
        pantalla.blit(fondo_desertico, (0, 0))
        pantalla.blit(oscurecedor, (0, 0))
        dibujar_texto("Ingresá tu nombre:", fuentes['mediana'], colores['negro'], 450, 200)
        input_rect = pygame.Rect(350, 270, 200, 50)
        pygame.draw.rect(pantalla, colores['blanco'], input_rect)
        dibujar_texto(nombre, fuentes['chica'], colores['negro'], 450, 297)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip():
                    nombre_final = nombre.strip()
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 20 and evento.unicode.isprintable():
                    nombre += evento.unicode
        clock.tick(60)

    return nombre_final


def ejecutar_menu_principal(nombre: str) -> None:
    """
    Muestra el menú principal del juego con opciones para jugar, ver estadísticas o salir.

    Args:
        nombre (str): Nombre del jugador.
    """
    opciones = ["Jugar Trivia", "Ver estadísticas","Minijuego Guardianes", "Ver ranking", "Salir"]
    ejecutando = True

    while ejecutando:
        pantalla.blit(cueva, (0,0))
        pantalla.blit(oscurecedor, (0, 0))
        dibujar_texto(f"Bienvenido, {nombre}", fuentes['grande'], colores['rojo'], 450, 120) # agrandar el binvenidos
        dibujar_texto("Menú Principal", fuentes['mediana'], colores['blanco'], 450, 200)

        botones = []        
        indice_opcion = 0
        cantidad_opciones = 0

        for texto in opciones:
            x = 270
            y = 150 + indice_opcion * 90
            w = 300
            h = 50

            rect = dibujar_boton(x, y, texto, colores["blanco"], fuentes["mediana"], boton_normal  )
            #pygame.draw.rect(pantalla, colores['blanco'], rect, border_radius=10)
            #dibujar_texto(texto, fuentes['chica'], colores['negro'],450 , y + 25)
            botones.append((rect, texto))

            indice_opcion = indice_opcion + 1
            cantidad_opciones = cantidad_opciones + 1

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                indice = 0
                for boton in botones:
                    rect = boton[0]
                    texto = boton[1]
                    if rect.collidepoint(evento.pos):
                        if texto == "Jugar Trivia":
                            iniciar_trivia(nombre)
                        elif texto == "Ver estadísticas":
                            mostrar_estadisticas_usuario_visual(nombre)
                        elif texto == "Ver ranking":
                            mostrar_ranking_visual()
                        elif texto == "Minijuego Guardianes":
                            jugar_guardianes_pygame()
                        elif texto == "Salir":
                            pygame.quit()
                            sys.exit()
                    indice = indice + 1

        clock.tick(60)


def mostrar_estadisticas_usuario_visual(nombre: str) -> None:
    """
    Muestra las estadísticas del usuario en pantalla.

    Args:
        nombre (str): Nombre del jugador.
    """
    stats = calcular_estadisticas(nombre, "Usuarios.json")
    pantalla.blit(pared_estadisticas, (0,0))
    pantalla.blit(oscurecedor, (0, 0))

    if "error" in stats:
        mensaje = stats["error"]
        dibujar_texto(mensaje, fuentes['mediana'], colores['rojo'], 450, 350)

    else:
        y = 60
        dibujar_texto(f"📊 ESTADÍSTICAS DE {nombre}", fuentes['grande'], colores['verde'], 450, y)
        y += 60
        dibujar_texto(f"🎮 Partidas: {stats['intentos']}", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"📈 Prom preguntas: {stats['promedio_preguntas_por_partida']}", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"🏆 Mejor puntaje: {stats['mejor_puntaje']}", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"📊 Promedio puntaje: {stats['promedio_puntaje']}", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"📊 Último puntaje: {stats['ultimo_puntaje']}", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"✅ Mejor %: {stats['mejor_porcentaje']}% | Prom %: {stats['promedio_porcentaje']}% | Último %: {stats['ultimo_porcentaje']}%", fuentes['chica'], colores['blanco'], 450, y); y += 30
        dibujar_texto(f"⏱️ Prom tiempo: {stats['promedio_tiempo']}s | Mejor: {stats['mejor_tiempo']}s", fuentes['chica'], colores['blanco'], 450, y)

    boton_volver = dibujar_texto("Volver al menú", fuentes["mediana"], colores['blanco'], 450, 640)
    pygame.display.flip()
    esperar_click([boton_volver]) 


def mostrar_ranking_visual() -> None:
    """
    Muestra el ranking de los jugadores con mejor puntaje.
    """
    ranking = ordenar_ranking(obtener_datos_ranking("Usuarios.json"))
    pantalla.blit(pared_estadisticas, (0,0))
    pantalla.blit(oscurecedor, (0, 0))
    y = 40
    dibujar_texto("🏆 RANKING DE JUGADORES", fuentes['grande'], colores['rojo'], 450, y)
    y = y + 40

    if not ranking:
        dibujar_texto("❌ No hay jugadores con estadísticas", fuentes['mediana'], colores['rojo'], 450, y)
    else:
        i = 0
        while i < 10:
            if i >= len(ranking):
                break

            usuario = ranking[i]
            y_offset = y + i * 55

            dibujar_texto(f"{i + 1}. {usuario['nombre']}", fuentes['chica'], colores['negro'], 150, y_offset)
            dibujar_texto(f"🏆 {usuario['mejor_puntaje']} pts", fuentes['chica'], colores['negro'], 400, y_offset)
            dibujar_texto(f"📈 {usuario['mejor_porcentaje']}% | 🎮 {usuario['intentos']} partidas", fuentes['chica'], colores['negro'], 600, y_offset)

            i = i + 1

        boton_volver = dibujar_texto("Volver al menú", fuentes["mediana"], colores['rojo'], 450, 640)
        pygame.display.flip()
        esperar_click([boton_volver]) 