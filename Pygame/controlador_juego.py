import time
import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preguntas import cargar_preguntas_con_opciones, seleccionar_pregunta_de_disponibles
from validaciones_y_prints import evaluar_respuesta_en_partida, calcular_racha_en_partida
from manejo_de_usuario import guardar_estadisticas_usuario
from utilidades_pygame import dibujar_texto, esperar_click, colores, fuentes, pantalla, clock, cueva, boton_normal, dibujar_boton


def iniciar_trivia(nombre: str) -> None:
    """
    Inicia el flujo principal de preguntas para el jugador.

    Args:
        nombre (str): Nombre del jugador.
    """
    preguntas = cargar_preguntas_con_opciones("Preguntas.csv")
    disponibles = preguntas.copy()
    respuestas = []

    tiempo_inicio = time.time()

    for nivel in [1, 2, 3]:
        por_nivel = []
        for p in disponibles.values():
            if p['nivel'] == nivel:
                por_nivel.append(p)

        if not por_nivel:
            continue

        for _ in range(2):
            racha_actual = calcular_racha_en_partida(respuestas)
            pregunta = seleccionar_pregunta_de_disponibles(disponibles)
            botones = mostrar_pregunta_visual(pregunta)
            seleccion = esperar_click(botones)
            letra = "ABCD"[seleccion]

            resultado = evaluar_respuesta_en_partida(
                letra,
                pregunta['opciones'],
                pregunta['correcta'],
                pregunta['nivel'],
                pregunta['dificultad'],
                racha_actual,
                nombre,
                mostrar_respuesta_correcta=True
            )

            mostrar_resultado_visual(resultado)
            resultado['pregunta_id'] = pregunta['id']
            respuestas.append(resultado)
            del disponibles[pregunta['id']]

    tiempo_total = time.time() - tiempo_inicio
    guardar_estadisticas_visual(nombre, respuestas, tiempo_total)
    mostrar_resumen_final(respuestas, tiempo_total, nombre)


def mostrar_pregunta_visual(pregunta: dict, seleccionada: int = None) -> list[pygame.Rect]:
    """
    Muestra en pantalla una pregunta y sus opciones.

    Args:
        pregunta (dict): Pregunta a mostrar.
        seleccionada (int, optional): Índice resaltado. Defaults to None.

    Returns:
        list[pygame.Rect]: Lista de botones clickeables.
    """
    pantalla.blit(cueva, (0,0))
    dibujar_texto(f"NIVEL {pregunta['nivel']} - {pregunta['categoria']}", fuentes['mediana'], colores['verde'], 450, 40)
    dibujar_texto(pregunta['descripcion'], fuentes['grande'], colores['blanco'], 450, 100)

    letras = "ABCD"
    botones = []
    indice = 0
    cantidad_opciones = 0
    for opcion in pregunta['opciones']:
        x = 260
        y = 180 + indice * 100
        w = 660
        h = 60

        if seleccionada is not None and seleccionada == indice:
            color = colores['verde']
        else:
            color = colores['blanco']

        rect = dibujar_boton(x, y, f"{letras[indice]}) {opcion}", color, fuentes["chica"], boton_normal)
        #pygame.draw.rect(pantalla, color, (x, y, w, h), border_radius=10)
        #dibujar_texto(f"{letras[indice]}) {opcion}", fuentes['chica'], colores['blanco'], x + 20, y + 15)
        botones.append(rect)

        indice = indice + 1
        cantidad_opciones = cantidad_opciones + 1

    pygame.display.flip()
    return botones


def mostrar_resultado_visual(resultado: dict) -> None:
    """
    Muestra el resultado de una respuesta: correcta o incorrecta.

    Args:
        resultado (dict): Resultado de la evaluación.
    """
    pantalla.fill(colores['gris'])
    color = colores['verde'] if resultado['es_correcta'] else colores['rojo']
    mensaje = resultado['mensaje'].split("\n")

    dibujar_texto(mensaje[0], fuentes['grande'], color, 450, 310)
    if len(mensaje) > 1:
        dibujar_texto(mensaje[1], fuentes['chica'], color, 450, 360)

    if resultado.get("puntos_buffeo", 0) > 0:
        dibujar_texto(f"Puntos base: {resultado['puntos_base']}", fuentes['chica'], colores['negro'], 450, 420)
        dibujar_texto(f"Buffeo: +{resultado['puntos_buffeo']}", fuentes['chica'], colores['azul'], 450, 460)

    dibujar_texto(f"Total: {resultado['puntos']} puntos", fuentes['mediana'], colores['negro'], 450, 520)
    pygame.display.flip()
    time.sleep(2)


def guardar_estadisticas_visual(nombre: str, respuestas: list[dict], tiempo_total: float) -> None:
    """
    Calcula resumen de partida y guarda las estadísticas del jugador.

    Args:
        nombre (str): Nombre del jugador.
        respuestas (list[dict]): Lista de respuestas registradas.
        tiempo_total (float): Tiempo total en segundos.
    """
    correctas = 0
    puntos = 0
    buffeo = 0
    total = 0

    for r in respuestas:
        total += 1
        puntos += r['puntos']
        buffeo += r.get('puntos_buffeo', 0)
        if r['es_correcta']:
            correctas += 1

    resumen = {
        "puntos_totales": puntos,
        "puntos_buffeo": buffeo,
        "respuestas_correctas": correctas,
        "total_preguntas": total,
        "tiempo_total_segundos": round(tiempo_total, 2),
        "detalle": respuestas
    }

    guardar_estadisticas_usuario(nombre, resumen, "Usuarios.json")


def mostrar_resumen_final(respuestas: list[dict], tiempo_total: float, nombre: str) -> None:
    """
    Muestra pantalla final de resumen de la trivia completada.

    Args:
        respuestas (list[dict]): Lista de respuestas de la partida.
        tiempo_total (float): Tiempo total en segundos.
        nombre (str): Nombre del jugador.
    """
    pantalla.fill(colores['blanco'])
    correctas = 0
    total = 0
    puntos = 0
    buffeo = 0

    for r in respuestas:
        total += 1
        puntos += r['puntos']
        buffeo += r.get('puntos_buffeo', 0)
        if r['es_correcta']:
            correctas += 1

    dibujar_texto("🏁 TRIVIA COMPLETADA", fuentes['grande'], colores['azul'], 450, 70)
    dibujar_texto(f"Jugador: {nombre}", fuentes['mediana'], colores['negro'], 450, 130)
    dibujar_texto(f"Correctas: {correctas}/{total}", fuentes['mediana'], colores['negro'], 450, 190)
    dibujar_texto(f"Puntos base: {puntos - buffeo}", fuentes['mediana'], colores['negro'], 450, 250)
    dibujar_texto(f"Buffeo: +{buffeo}", fuentes['mediana'], colores['azul'], 450, 310)
    dibujar_texto(f"Total: {puntos} puntos", fuentes['mediana'], colores['negro'], 450, 370)
    dibujar_texto(f"Tiempo: {round(tiempo_total, 2)} seg", fuentes['mediana'], colores['gris'], 450, 430)

    if total > 0:
        porcentaje = round((correctas / total) * 100, 1)
        dibujar_texto(f"Aciertos: {porcentaje}%", fuentes['mediana'], colores['azul'], 450, 490)

    boton_volver = dibujar_texto("Volver al menú", fuentes["mediana"], colores['rojo'], 450, 640)
    pygame.display.flip()
    esperar_click([boton_volver]) 

    clock.tick(60)