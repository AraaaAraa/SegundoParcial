from verificacion_archivos import verificar_archivo_existe, cargar_json, guardar_json
from generales import calcular_estadisticas_lista
from prints_de_juego import pedir_nombre_usuario, imprimir_estadisticas
import os

USUARIOS_PATH = os.path.join(os.path.dirname(__file__), "Usuarios.json")



def obtener_datos_usuario(nombre_usuario: str, archivo: str) -> dict:
    resultado = {"error": ""}
    
    if verificar_archivo_existe(archivo, "No hay estadísticas guardadas") == False:
        resultado["error"] = "No hay estadísticas guardadas"
    else:
        datos = cargar_json(archivo)
        if not datos:
            resultado["error"] = "Error al cargar estadísticas"
        else:
            # Buscar el usuario iterando por las claves del diccionario
            usuario_encontrado = False
            for clave in datos:
                if clave == nombre_usuario:
                    usuario_encontrado = True
                    break
            
            if not usuario_encontrado:
                resultado["error"] = "Usuario '" + nombre_usuario + "' no encontrado"
            else:
                resultado = datos[nombre_usuario]
    
    return resultado

def obtener_stats_desde_lista(usuario: dict, clave: str) -> dict:
    resultado = None
    clave_encontrada = False
    
    # Buscar la clave iterando por las claves del diccionario
    for clave_dict in usuario:
        if clave_dict == clave:
            clave_encontrada = True
            break
    
    if clave_encontrada and len(usuario[clave]) > 0:
        resultado = calcular_estadisticas_lista(usuario[clave])
    else:
        resultado = calcular_estadisticas_lista([])
    
    return resultado

def obtener_ultimo_valor(usuario: dict, clave: str) -> float:
    resultado = 0.0
    clave_encontrada = False
    
    # Buscar la clave iterando por las claves del diccionario
    for clave_dict in usuario:
        if clave_dict == clave:
            clave_encontrada = True
            break
    
    if clave_encontrada and len(usuario[clave]) > 0:
        resultado = usuario[clave][-1]
    else:
        resultado = 0
    
    return resultado


def obtener_valor_directo(usuario: dict, clave: str) -> int:
    resultado = 0
    clave_encontrada = False
    
    # Buscar la clave iterando por las claves del diccionario
    for clave_dict in usuario:
        if clave_dict == clave:
            clave_encontrada = True
            break
    
    if clave_encontrada:
        resultado = usuario[clave]
    else:
        resultado = 0
    
    return resultado



def calcular_estadisticas(nombre_usuario: str, archivo_usuarios: str) -> dict:
    usuario = obtener_datos_usuario(nombre_usuario, archivo_usuarios)
    
    # Buscar la clave "error" iterando por las claves del diccionario
    tiene_error = False
    for clave in usuario:
        if clave == "error":
            tiene_error = True
            break
    
    resultado = None
    
    if tiene_error:
        resultado = {"error": usuario["error"]}
    else:
        stats = calcular_todas_las_estadisticas(usuario)
        resultado = construir_diccionario_estadisticas(nombre_usuario, usuario, stats)
    
    return resultado


def calcular_todas_las_estadisticas(usuario: dict) -> dict:
    retoto = {
        "puntajes": obtener_stats_desde_lista(usuario, "puntajes"),
        "tiempos": obtener_stats_desde_lista(usuario, "tiempos"),
        "aciertos": obtener_stats_desde_lista(usuario, "aciertos"),
        "porcentajes": obtener_stats_desde_lista(usuario, "porcentajes"),
        "total_preguntas": obtener_stats_desde_lista(usuario, "total_preguntas"),
        "ultimo_puntaje": obtener_ultimo_valor(usuario, "puntajes"),
        "ultimo_porcentaje": obtener_ultimo_valor(usuario, "porcentajes"),
        "intentos": obtener_valor_directo(usuario, "intentos")
    }
    return retoto



def construir_diccionario_estadisticas(nombre_usuario: str, usuario: dict, stats: dict) -> dict:
    return {
        "nombre": nombre_usuario,
        "intentos": stats["intentos"],
        "promedio_puntaje": round(stats["puntajes"]["promedio"], 2),
        "promedio_tiempo": round(stats["tiempos"]["promedio"], 2),
        "promedio_aciertos": round(stats["aciertos"]["promedio"], 2),
        "promedio_porcentaje": round(stats["porcentajes"]["promedio"], 2),
        "mejor_puntaje": stats["puntajes"]["mejor"],
        "mejor_porcentaje": stats["porcentajes"]["mejor"],
        "mejor_tiempo": stats["tiempos"]["peor"],
        "ultimo_puntaje": stats["ultimo_puntaje"],
        "ultimo_porcentaje": stats["ultimo_porcentaje"],
        "promedio_preguntas_por_partida": round(stats["total_preguntas"]["promedio"], 1),
        "historial_completo": usuario
    }



def inicializar_datos_usuario(nombre: str, datos: dict) -> dict:
    resultado = None
    usuario_encontrado = False
    
    # Buscar el nombre de usuario iterando por las claves del diccionario
    for clave in datos:
        if clave == nombre:
            usuario_encontrado = True
            break
    
    if usuario_encontrado:
        resultado = datos
    else:
        datos[nombre] = {
            "intentos": 0,
            "puntajes": [],
            "tiempos": [],
            "aciertos": [],
            "total_preguntas": [],
            "porcentajes": [],
            "historial": []
        }
        resultado = datos
    
    return resultado


def actualizar_listas_estadisticas(usuario: dict, resultado: dict) -> dict:
    usuario["intentos"] = usuario["intentos"] + 1
    usuario["puntajes"].append(resultado["puntos_totales"])
    usuario["tiempos"].append(resultado["tiempo_total_segundos"])
    usuario["aciertos"].append(resultado["respuestas_correctas"])
    usuario["total_preguntas"].append(resultado["total_preguntas"])
    
    porcentaje = 0
    if resultado["total_preguntas"] > 0:
        porcentaje = (resultado["respuestas_correctas"] / resultado["total_preguntas"]) * 100
    usuario["porcentajes"].append(round(porcentaje, 1))
    usuario["historial"].append(resultado["detalle"])

    return usuario




def guardar_estadisticas_usuario(nombre_usuario: str, resultado: dict, archivo_usuarios: str) -> None:
    datos = cargar_json(archivo_usuarios, {})
    datos = inicializar_datos_usuario(nombre_usuario, datos)
    usuario = datos[nombre_usuario]
    usuario = actualizar_listas_estadisticas(usuario, resultado)
    datos[nombre_usuario] = usuario
    guardar_json(archivo_usuarios, datos)
    return None



def obtener_datos_ranking(archivo: str) -> list:
    datos = cargar_json(archivo)
    ranking = []
    
    if datos:
        for nombre in datos:
            stats = datos[nombre]
            
            # Verificar si existe "puntajes" y tiene elementos
            tiene_puntajes = False
            for clave in stats:
                if clave == "puntajes":
                    tiene_puntajes = True
                    break
            
            if tiene_puntajes and len(stats["puntajes"]) > 0:
                stats_puntajes = calcular_estadisticas_lista(stats["puntajes"])
                
                # Verificar si existe "porcentajes"
                tiene_porcentajes = False
                for clave in stats:
                    if clave == "porcentajes":
                        tiene_porcentajes = True
                        break
                
                if tiene_porcentajes:
                    stats_porcentajes = calcular_estadisticas_lista(stats["porcentajes"])
                else:
                    stats_porcentajes = {"mejor": 0, "promedio": 0}
                
                # Verificar si existe "intentos"
                intentos = 0
                for clave in stats:
                    if clave == "intentos":
                        intentos = stats["intentos"]
                        break
                
                ranking.append({
                    "nombre": nombre,
                    "mejor_puntaje": stats_puntajes["mejor"],
                    "promedio_puntaje": round(stats_puntajes["promedio"], 2),
                    "mejor_porcentaje": stats_porcentajes["mejor"],
                    "promedio_porcentaje": round(stats_porcentajes["promedio"], 1),
                    "intentos": intentos
                })
    
    return ranking

def ordenar_ranking(ranking: list) -> list:
    ordenado = []
    for usuario in ranking:
        insertado = False
        nueva_lista_ordenada = []
        i = 0
        while i < len(ordenado):
            if not insertado and usuario["mejor_puntaje"] > ordenado[i]["mejor_puntaje"]:
                nueva_lista_ordenada.append(usuario)
                insertado = True
            nueva_lista_ordenada.append(ordenado[i])
            i = i + 1
        if not insertado:
            nueva_lista_ordenada.append(usuario)
        ordenado = nueva_lista_ordenada
    return ordenado

def imprimir_ranking(usuarios: list) -> None:
    print("\n" + "=" * 60)
    print("🏆 RANKING DE JUGADORES")
    print("=" * 60)

    if len(usuarios) == 0:
        print("❌ No hay jugadores con estadísticas")
    else:
        i = 0
        while i < len(usuarios):
            usuario = usuarios[i]
            posicion = i + 1
            print(f"{posicion}. {usuario['nombre']}")
            print(f"   🏆 Mejor puntaje: {usuario['mejor_puntaje']}")
            print(f"   📊 Promedio: {usuario['promedio_puntaje']}")
            print(f"   📈 Mejor %: {usuario['mejor_porcentaje']}%")
            print(f"   🎮 Partidas: {usuario['intentos']}")
            print("-" * 40)
            i = i + 1
    return None


def mostrar_ranking_usuarios(archivo_usuarios: str = USUARIOS_PATH) -> None:
    existe = verificar_archivo_existe(archivo_usuarios, "No hay estadísticas guardadas")
    if existe:
        ranking = obtener_datos_ranking(archivo_usuarios)
        ordenado = ordenar_ranking(ranking)
        imprimir_ranking(ordenado)
    return None

def mostrar_estadisticas_usuario(nombre: str = "", archivo_usuarios: str = None) -> None:
    if not nombre:
        nombre = pedir_nombre_usuario()
    if not archivo_usuarios:
        archivo_usuarios = USUARIOS_PATH

    estadisticas = calcular_estadisticas(nombre, archivo_usuarios)

    if "error" in estadisticas:
        print(f"❌ {estadisticas['error']}")
    else:
        imprimir_estadisticas(estadisticas)




