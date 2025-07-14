from generales import convertir_a_mayusculas, quitar_espacios_extremos
from typing import Dict



def mostrar_pregunta(pregunta: Dict) -> str:
    print("\n🎯 NIVEL " + str(pregunta['nivel']) + " - " + convertir_a_mayusculas(pregunta['categoria']))
    print("📝 " + pregunta['descripcion'])
    print()
    opciones = pregunta['opciones']
    letras = "ABCD"
    i = 0
    while i < len(opciones):
        print(letras[i] + ") " + opciones[i])
        i = i + 1
    respuesta = input("\n🤔 Tu respuesta (A/B/C/D): ")
    respuesta = convertir_a_mayusculas(quitar_espacios_extremos(respuesta))
    return respuesta




def mostrar_resultado_parcial(resultado: dict) -> None:
    print("\n" + resultado["mensaje"])
    
    puntos_buffeo = 0
    # Buscar la clave "puntos_buffeo" iterando por las claves del diccionario
    for clave in resultado:
        if clave == "puntos_buffeo":
            puntos_buffeo = resultado["puntos_buffeo"]
            break
    
    if puntos_buffeo > 0:
        # Buscar puntos_base o usar 0 como valor por defecto
        puntos_base = 0
        for clave in resultado:
            if clave == "puntos_base":
                puntos_base = resultado["puntos_base"]
                break
        
        print(f"📊 Puntos base: {puntos_base}")
        print(f"🔥 Puntos buffeo: +{puntos_buffeo}")
        print(f"📊 Puntos totales: {resultado['puntos']}")
    else:
        print("📊 Puntos obtenidos: " + str(resultado["puntos"]))
    
    resultado_return = None
    return resultado_return



def mostrar_cabecera_nivel(nivel: int) -> None:
    print("\n" + "=" * 30)
    print("🎯 PREGUNTA NIVEL " + str(nivel))
    print("=" * 30)
    return None



def mostrar_resumen_con_buffeo(nombre, respuestas_correctas, total_preguntas, puntos_totales, puntos_buffeo, tiempo_total) -> None:
    print("\n" + "="*50)
    print("🏁 RESUMEN FINAL")
    print("="*50)
    print("👤 Jugador: " + nombre)
    print("✅ Respuestas correctas: " + str(respuestas_correctas) + "/" + str(total_preguntas))
    print("📊 Puntos base: " + str(puntos_totales - puntos_buffeo))
    if puntos_buffeo > 0:
        print("🔥 Puntos por buffeo: +" + str(puntos_buffeo))
    print("📊 Puntos totales: " + str(puntos_totales))
    print("⏱️ Tiempo total: " + str(round(tiempo_total, 2)) + " segundos")
    if total_preguntas > 0:
        porcentaje = (respuestas_correctas / total_preguntas) * 100
        print("📈 Porcentaje de aciertos: " + str(round(porcentaje, 1)) + "%")

def imprimir_estadisticas(stats: dict) -> None:
    print(f"\n📊 === ESTADÍSTICAS DE {stats['nombre']} ===")
    print(f"🎮 Partidas jugadas: {stats['intentos']}")
    print(f"📈 Promedio preguntas por partida: {stats['promedio_preguntas_por_partida']}")
    print()
    imprimir_puntajes(stats)
    imprimir_aciertos(stats)
    imprimir_tiempos(stats)




def imprimir_puntajes(stats: dict) -> None:
    print("🏆 PUNTAJES:")
    print(f"   • Mejor puntaje: {stats['mejor_puntaje']}")
    print(f"   • Promedio: {stats['promedio_puntaje']}")
    print(f"   • Último: {stats['ultimo_puntaje']}")
    print()




def imprimir_aciertos(stats: dict) -> None:
    print("✅ ACIERTOS:")
    print(f"   • Mejor porcentaje: {stats['mejor_porcentaje']}%")
    print(f"   • Promedio porcentaje: {stats['promedio_porcentaje']}%")
    print(f"   • Último porcentaje: {stats['ultimo_porcentaje']}%")
    print(f"   • Promedio respuestas correctas: {stats['promedio_aciertos']}")
    print()




def imprimir_tiempos(stats: dict) -> None:
    print("⏱️ TIEMPOS:")
    print(f"   • Mejor tiempo: {stats['mejor_tiempo']} segundos")
    print(f"   • Promedio: {stats['promedio_tiempo']} segundos")



def pedir_nombre_usuario() -> None:
    while True:
        nombre = input("🗡️ Ingresá tu nombre de usuario: ")
        nombre = quitar_espacios_extremos(nombre)
        if nombre:
            return nombre
        print("🗡️ El nombre no puede estar vacío. Intentá de nuevo.")