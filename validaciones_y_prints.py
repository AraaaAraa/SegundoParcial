from prints_de_juego import mostrar_pregunta, mostrar_resultado_parcial
from puntaje import calcular_puntaje_total, calcular_puntos_base
from generales  import obtener_indice_letra
from buffeos import verificar_objeto_excepcional, usar_armadura_si_disponible, aplicar_buffeo_en_partida, usar_bolsa_monedas_si_disponible, usar_raciones_si_disponible, calcular_buffeo_reintento
import time
import os

BASE_DIR = os.path.dirname(__file__)
ESTADO_BUFF_PATH = os.path.join(BASE_DIR, "EstadoBuff.json")

def validar_indice(indice: int, opciones: list) -> bool:
    es_valido = 0 <= indice < len(opciones)
    return es_valido

def puede_usar_reintento_en_partida(racha_actual: int, nombre_usuario: str, estado_buff_path: str) -> bool:
    objeto = verificar_objeto_excepcional(nombre_usuario, estado_buff_path)
    resultado = calcular_buffeo_reintento(racha_actual, objeto)
    return resultado == -1

def evaluar_respuesta_en_partida(
    respuesta_usuario: str,
    opciones: list,
    respuesta_correcta: str,
    nivel: int,
    dificultad: int,
    racha_actual: int,
    nombre_usuario: str,
    mostrar_respuesta_correcta: bool = True
) -> dict:
    indice = obtener_indice_letra(respuesta_usuario)
    es_valido = validar_indice(indice, opciones)

    if not es_valido:
        resultado = construir_resultado_no_valido()
    else:
        seleccion = opciones[indice]
        es_correcta = verificar_respuesta_con_armadura(seleccion, respuesta_correcta, nombre_usuario)
        puntos = calcular_puntaje_total(es_correcta, dificultad, racha_actual, nombre_usuario)
        mensaje = construir_mensaje(nivel, es_correcta, respuesta_correcta, mostrar_respuesta_correcta)
        resultado = construir_resultado_valido(seleccion, es_correcta, mensaje, puntos)

    return resultado

def verificar_respuesta_con_armadura(seleccion: str, correcta: str, nombre: str) -> bool:
    es_correcta = seleccion == correcta
    es_correcta, _ = usar_armadura_si_es_necesario(nombre, es_correcta)
    return es_correcta



def calcular_puntaje_total(
    es_correcta: bool,
    dificultad: int,
    racha_actual: int,
    nombre: str
) -> dict:
    puntos_base = calcular_puntos_base(es_correcta, dificultad)
    puntos_buffeo = aplicar_buffeo_en_partida(es_correcta, "puntos_extra", racha_actual, nombre)
    puntos_raciones = usar_raciones_si_disponible(nombre, es_correcta)
    puntos_bolsa = usar_bolsa_monedas_si_disponible(nombre, es_correcta, puntos_base)

    puntos = {
        "puntos": puntos_base + puntos_buffeo + puntos_raciones + puntos_bolsa,
        "puntos_base": puntos_base,
        "puntos_buffeo": puntos_buffeo
    }

    return puntos



def construir_resultado_valido(
    seleccion: str,
    es_correcta: bool,
    mensaje: str,
    puntos: dict
) -> dict:
    resultado = {
        "valida": True,
        "es_correcta": es_correcta,
        "mensaje": mensaje,
        "puntos": puntos["puntos"],
        "puntos_base": puntos["puntos_base"],
        "puntos_buffeo": puntos["puntos_buffeo"],
        "seleccion": seleccion
    }

    return resultado



def construir_resultado_no_valido() -> dict:
    return {
        "valida": False,
        "es_correcta": False,
        "mensaje": "❌ Opción inválida.",
        "puntos": 0,
        "puntos_base": 0,
        "puntos_buffeo": 0,
        "seleccion": ""
    }

def construir_mensaje(nivel: int, es_correcta: bool, respuesta_correcta: str, mostrar_respuesta_correcta: bool = True) -> str:
    mensaje = ""
    
    # Determinar el mensaje base usando condicionales
    if nivel == 1:
        if es_correcta:
            mensaje = "✅ CORRECTO\nFELICIDADES NO SOS UN BURRO!!!"
        else:
            mensaje = "❌ INCORRECTO\nSos un burro"
    elif nivel == 2:
        if es_correcta:
            mensaje = "✅ CORRECTO\nFuaaaa qué inteligente!!!"
        else:
            mensaje = "❌ INCORRECTO\nBue... ¿qué pasó?"
    elif nivel == 3:
        if es_correcta:
            mensaje = "✅ CORRECTO\nNi yo la sabía!!!"
        else:
            mensaje = "❌ INCORRECTO\nTe entiendo la verdad"
    
    # Agregar respuesta correcta si es necesario
    if not es_correcta and mostrar_respuesta_correcta:
        mensaje += "\n💡 La respuesta correcta era: " + respuesta_correcta
    
    return mensaje

def procesar_intentos_en_partida(pregunta: dict, max_intentos: int, racha_actual: int, nombre_usuario: str, estado_buff_path: str) -> dict:
    intentos = 0
    respuesta = ""
    resultado = {}
    duracion = 0
    terminado = False

    while intentos < max_intentos and not terminado:
        duracion = medir_duracion_respuesta(intentos)
        respuesta = mostrar_pregunta(pregunta)
        puede_reintentar = puede_usar_reintento_en_partida(racha_actual, nombre_usuario, estado_buff_path)
        es_ultimo_intento = (intentos >= max_intentos - 1) and not puede_reintentar
        mostrar_respuesta_correcta = es_ultimo_intento

        resultado = evaluar_respuesta_en_partida(
            respuesta,
            pregunta["opciones"],
            pregunta["correcta"],
            pregunta["nivel"],
            pregunta["dificultad"],
            racha_actual,
            nombre_usuario,
            mostrar_respuesta_correcta
        )

        mostrar_resultado_parcial(resultado)

        if not resultado["valida"]:
            continue

        if resultado["es_correcta"]:
            terminado = True
        else:
            if es_ultimo_intento:
                terminado = True
            elif puede_reintentar:
                desea_reintentar = deberia_reintentar(nombre_usuario)
                if desea_reintentar:
                    intentos += 1
                    continue
                else:
                    terminado = True
            else:
                terminado = True
        intentos += 1

    resultado_final = {
        "respuesta": respuesta,
        "resultado": resultado,
        "duracion": duracion,
        "intentos_usados": intentos,
        "fue_error": not resultado["es_correcta"]
    }
    return resultado_final



def medir_duracion_respuesta(intentos: int) -> float:
    if intentos > 0:
        print("\n🛡️ REINTENTO #" + str(intentos + 1))
        print("=" * 20)
    inicio = time.time()
    fin = time.time()
    duracion = round(fin - inicio, 2)
    return duracion



def verificar_si_termina(resultado: dict, intentos: int, max_intentos: int, racha_actual: int, nombre_usuario: str, estado_buff_path: str) -> bool:
    termino = False
    if resultado["es_correcta"] or intentos == max_intentos - 1:
        termino = True
    elif not puede_usar_reintento_en_partida(racha_actual, nombre_usuario, estado_buff_path):
        termino = True
    return termino



def deberia_reintentar(nombre_usuario: str) -> bool:
    usar_reintento = input("\n🛡️ ¿Quieres usar tu buffeo de reintento? (s/n) : ").lower().strip()
    retornos = False
    if usar_reintento == "s":
        print("🔄 Usando reintento...")
        retornos = True
    return retornos



def calcular_racha_en_partida(respuestas_actuales: list) -> int:
    if not respuestas_actuales:
        return 0
    
    racha_actual = 0
    i = len(respuestas_actuales) - 1
    
    while i >= 0:
        respuesta = respuestas_actuales[i]
        es_correcta = False
        for clave in respuesta:
            if clave == "es_correcta":
                es_correcta = respuesta[clave]
                break
        
        if es_correcta:
            racha_actual += 1
        else:
            break
        
        i -= 1
    
    return racha_actual



def verificar_respuesta_con_armadura(seleccion: str, respuesta_correcta: str, nombre_usuario: str) -> bool:
    es_correcta = seleccion == respuesta_correcta
    if not es_correcta:
        es_correcta_con_armadura, _ = usar_armadura_si_es_necesario(nombre_usuario, es_correcta)
        es_correcta = es_correcta_con_armadura
    return es_correcta



def verificar_respuesta(seleccion: str, respuesta_correcta: str) -> bool:
    return seleccion == respuesta_correcta



def usar_armadura_si_es_necesario(nombre_usuario: str, es_correcta: bool) -> tuple:
    if es_correcta:
        return True, False
    armadura_usada = usar_armadura_si_disponible(nombre_usuario, es_correcta)
    return (True, True) if armadura_usada else (False, False)
