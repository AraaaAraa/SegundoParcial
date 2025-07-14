import os
from manejo_de_usuario import guardar_estadisticas_usuario
from preguntas import filtrar_preguntas_disponibles, cargar_preguntas_con_opciones, seleccionar_pregunta_de_disponibles
from buffeos import verificar_y_otorgar_objeto_excepcional, verificar_objeto_excepcional
from prints_de_juego import mostrar_cabecera_nivel, mostrar_resumen_con_buffeo
from validaciones_y_prints import procesar_intentos_en_partida, puede_usar_reintento_en_partida, calcular_racha_en_partida

BASE_DIR = os.path.dirname(__file__)
ESTADO_BUFF_PATH = os.path.join(BASE_DIR, "EstadoBuff.json")


def jugar_ronda_sin_repetir_en_partida(preguntas: dict, nivel: int, preguntas_usadas: list, racha_actual: int, nombre_usuario: str, estado_buff_path: str) -> dict:
    mostrar_cabecera_nivel(nivel)

    pregunta = obtener_pregunta_disponible(preguntas, nivel, preguntas_usadas)
    if pregunta is None:
        resultado = None
        return resultado

    max_intentos = determinar_maximos_intentos(racha_actual, nombre_usuario, estado_buff_path)
    intento_info = procesar_intentos_en_partida(pregunta, max_intentos, racha_actual, nombre_usuario, estado_buff_path)
    
    puntos_base = obtener_valor_con_fallback(intento_info["resultado"], "puntos_base", "puntos")
    puntos_buffeo = intento_info["resultado"].get("puntos_buffeo", 0)

    resultado_completo = construir_resultado_completo(pregunta, nivel, intento_info, puntos_base, puntos_buffeo)

    return resultado_completo

def obtener_pregunta_disponible(preguntas: dict, nivel: int, preguntas_usadas: list) -> dict:
    preguntas_disponibles = filtrar_preguntas_disponibles(preguntas, nivel, preguntas_usadas)
    if not preguntas_disponibles:
        print("❌ No hay más preguntas disponibles para el nivel " + str(nivel))
        return None

    pregunta = seleccionar_pregunta_de_disponibles(preguntas_disponibles)
    if not pregunta:
        print("❌ No hay preguntas disponibles para el nivel " + str(nivel))
        return None

    return pregunta

def determinar_maximos_intentos(racha_actual: int, nombre_usuario: str, estado_buff_path: str) -> int:
    # Importar la función para verificar objetos
    from buffeos import verificar_objeto_excepcional
    retu = 1
    objeto = verificar_objeto_excepcional(nombre_usuario, estado_buff_path)
    if objeto == "espada":
        retu = 2
    return retu

def obtener_valor_con_fallback(diccionario: dict, clave_principal: str, clave_secundaria: str):
    if clave_principal in diccionario:
        return diccionario[clave_principal]
    return diccionario[clave_secundaria]

def construir_resultado_completo(pregunta: dict, nivel: int, intento_info: dict, puntos_base: int, puntos_buffeo: int) -> dict:
    resultado = intento_info["resultado"]
    
    resultado_completo = {
        "pregunta_id": pregunta["id"],
        "nivel": nivel,
        "respuesta_usuario": intento_info["respuesta"],
        "tiempo_segundos": intento_info["duracion"],
        "valida": resultado["valida"],
        "es_correcta": resultado["es_correcta"],
        "mensaje": resultado["mensaje"],
        "puntos": resultado["puntos"],
        "puntos_base": puntos_base,
        "puntos_buffeo": puntos_buffeo,
        "seleccion": resultado["seleccion"],
        "intentos_usados": intento_info["intentos_usados"]
    }

    return resultado_completo


def obtener_configuracion_niveles() -> dict:
    return {1: 5, 2: 3, 3: 2}

def procesar_nivel_en_partida(
    nivel: int,
    cantidad_preguntas: int,
    preguntas: dict,
    preguntas_usadas: list,
    nombre_usuario: str,
    respuestas_partida_actual: list
) -> dict:
    mostrar_inicio_de_nivel(nivel, cantidad_preguntas)

    respuestas = []
    total_puntos = 0
    total_buffeo = 0
    correctas = 0
    tiempo = 0

    i = 0
    while i < cantidad_preguntas:
        mostrar_encabezado_pregunta(i, cantidad_preguntas)

        racha_actual = calcular_racha_en_partida(respuestas_partida_actual)
        mostrar_racha_si_corresponde(racha_actual)

        resultado = jugar_ronda_sin_repetir_en_partida(preguntas, nivel, preguntas_usadas, racha_actual, nombre_usuario, ESTADO_BUFF_PATH)

        if resultado is not None:
            respuestas.append(resultado)
            respuestas_partida_actual.append(resultado)
            total_puntos, total_buffeo, tiempo, correctas = actualizar_estadisticas_parciales(
                resultado, total_puntos, total_buffeo, tiempo, correctas
            )
            preguntas_usadas.append(resultado["pregunta_id"])

        i = i + 1

    resultado_nivel = construir_resultado_nivel(respuestas, total_puntos, total_buffeo, correctas, tiempo)
    return resultado_nivel

def mostrar_inicio_de_nivel(nivel: int, cantidad: int):
    print("\n🎯 === NIVEL " + str(nivel) + " === 🎯")
    print("Responderás " + str(cantidad) + " preguntas de este nivel")

def mostrar_encabezado_pregunta(indice: int, total: int):
    print("\n--- Pregunta " + str(indice + 1) + " de " + str(total) + " ---")

def mostrar_racha_si_corresponde(racha: int):
    if racha > 0:
        print("🔥 Racha actual: " + str(racha) + " respuestas correctas")

def actualizar_estadisticas_parciales(resultado: dict, puntos: int, buffeo: int, tiempo_total: float, correctas: int):
    puntos = puntos + resultado["puntos"]
    buffeo = buffeo + resultado.get("puntos_buffeo", 0)
    tiempo_total = tiempo_total + resultado["tiempo_segundos"]
    if resultado["es_correcta"]:
        correctas = correctas + 1
    return puntos, buffeo, tiempo_total, correctas

def construir_resultado_nivel(respuestas: list, puntos: int, buffeo: int, correctas: int, tiempo: float) -> dict:
    return {
        "respuestas": respuestas,
        "total_puntos": puntos,
        "total_buffeo": buffeo,
        "correctas": correctas,
        "tiempo": tiempo
    }

def mostrar_inicio_de_partida():
    print("\n" + "=" * 50)
    print("🎮 INICIANDO PARTIDA")
    print("=" * 50)


def jugar_partida_y_guardar_estadisticas_nueva(nombre: str, archivo_usuarios: str, archivo_preguntas: str) -> str:
    mostrar_inicio_de_partida()

    preguntas = cargar_preguntas_con_opciones(archivo_preguntas)
    configuracion = obtener_configuracion_niveles()

    respuestas_totales, puntos, buffeo, correctas, tiempo = procesar_todos_los_niveles(
        preguntas, configuracion, nombre
    )

    total_preguntas = contar_preguntas(respuestas_totales)

    verificar_y_otorgar_objeto_excepcional(nombre, correctas, total_preguntas)

    estadisticas = construir_datos_estadisticos(
        puntos, buffeo, correctas, total_preguntas, tiempo, respuestas_totales
    )

    guardar_estadisticas_usuario(nombre, estadisticas, archivo_usuarios)
    mostrar_resumen_con_buffeo(nombre, correctas, total_preguntas, puntos, buffeo, tiempo)

    resultado = nombre
    return resultado

def procesar_todos_los_niveles(preguntas: dict, config: dict, nombre: str):
    preguntas_usadas = []
    respuestas_partida_actual = []
    todas_respuestas = []
    total_puntos = 0
    total_buffeo = 0
    total_correctas = 0
    total_tiempo = 0
    errores_acumulados = 0

    for nivel in [1, 2, 3]:
        info = jugar_y_procesar_nivel(nivel, config, preguntas, preguntas_usadas, nombre, respuestas_partida_actual)

        total_puntos, total_buffeo, total_correctas, total_tiempo = acumular_resultados_nivel(
            info, total_puntos, total_buffeo, total_correctas, total_tiempo
        )

        todas_respuestas = todas_respuestas + info["respuestas"]

        errores_acumulados = contar_errores_en_respuestas(info["respuestas"], errores_acumulados)
        if errores_acumulados >= 2:
            print("\n❌ Has fallado 2 veces. Fin de la partida.")
            break

    return todas_respuestas, total_puntos, total_buffeo, total_correctas, total_tiempo
def jugar_y_procesar_nivel(nivel: int, config: dict, preguntas: dict, preguntas_usadas: list, nombre: str, respuestas_partida_actual: list) -> dict:
    return procesar_nivel_en_partida(
        nivel,
        config[nivel],
        preguntas,
        preguntas_usadas,
        nombre,
        respuestas_partida_actual
    )


def acumular_resultados_nivel(info: dict, puntos: int, buffeo: int, correctas: int, tiempo: float) -> tuple:
    puntos = puntos + info["total_puntos"]
    buffeo = buffeo + info["total_buffeo"]
    correctas = correctas + info["correctas"]
    tiempo = tiempo + info["tiempo"]
    return puntos, buffeo, correctas, tiempo


def contar_errores_en_respuestas(respuestas: list, errores_actuales: int) -> int:
    for respuesta in respuestas:
        if not respuesta["es_correcta"]:
            errores_actuales += 1
    return errores_actuales

def contar_preguntas(respuestas: list) -> int:
    cantidad = 0
    i = 0
    while i < len(respuestas):
        cantidad = cantidad + 1
        i = i + 1
    return cantidad

def construir_datos_estadisticos(
    puntos: int,
    buffeo: int,
    correctas: int,
    total_preguntas: int,
    tiempo: float,
    respuestas: list
) -> dict:
    return {
        "puntos_totales": puntos,
        "puntos_buffeo": buffeo,
        "respuestas_correctas": correctas,
        "total_preguntas": total_preguntas,
        "tiempo_total_segundos": tiempo,
        "detalle": respuestas
    }