from generales import quitar_espacios_extremos
from verificacion_archivos import cargar_json, guardar_json, verificar_archivo_existe



def aplicar_buffeo_en_partida(resultado: bool, tipo_buffeo: str, racha_actual: int, nombre_usuario: str) -> int:
    objeto = verificar_objeto_excepcional(nombre_usuario, ESTADO_BUFF_PATH)
    buffeo = 0

    if tipo_buffeo == "puntos_extra" and resultado == True:
        buffeo = calcular_buffeo_puntos(racha_actual, objeto)
        imprimir_buffeo_puntos(buffeo, racha_actual, objeto)

    elif tipo_buffeo == "reintento" and resultado == False:
        buffeo = calcular_buffeo_reintento(racha_actual, objeto)
        if buffeo == -1:
            imprimir_buffeo_reintento(racha_actual, objeto)

    resultado_final = buffeo
    return resultado_final



def calcular_buffeo_puntos(racha_actual: int, objeto: str) -> int:
    puntos = 0
    if racha_actual > 7:
        puntos = 5
    elif racha_actual > 5:
        puntos = 3
    elif racha_actual > 3:
        puntos = 1

    if objeto == "espada":
        puntos = puntos + 2

    return puntos



def imprimir_buffeo_puntos(puntos: int, racha: int, objeto: str) -> None:
    if puntos == 0:
        return
    if objeto == "espada":
        print("⚔️ ¡ESPADA ACTIVADA! +2 puntos extra por la espada")
        print(f"\n🔥 ¡BUFFEO TOTAL! Has recibido {puntos} puntos extra (racha: {puntos - 2}, espada: +2)!")
    else:
        print(f"\n🔥 ¡BUFFEO ACTIVADO! Has recibido {puntos} puntos extra por tu racha de {racha} respuestas correctas!")



def calcular_buffeo_reintento(racha_actual: int, objeto: str) -> int:
    if racha_actual > 1 or objeto == "espada":
        return -1
    return 0



def imprimir_buffeo_reintento(racha: int, objeto: str) -> None:
    if racha > 1:
        print(f"\n🛡️ ¡BUFFEO DE REINTENTO! Tienes derecho a un reintento gracias a tu racha de {racha} respuestas correctas.")
    elif objeto == "espada":
        print("\n⚔️ ¡REINTENTO DE ESPADA! Tienes derecho a un reintento especial gracias a tu espada!")




def preguntar_espada_armadura() -> str:
    resultado = ""
    while resultado == "":
        print("\nHas obtenido una recompensa EXCEPCIONAL de Esfinge:")
        print("Elige tu objeto:")
        print("1)  Espada (2 puntos extra por respuesta correcta y un reintento especial disponible)")
        print("2)  Armadura (una protección automática contra una respuesta incorrecta)")
        print("3)  Raciones (recupera 3 puntos de vida cuando falles una pregunta)")
        print("4)  Bolsa de Monedas (duplica los puntos de la última pregunta correcta)")
        eleccion = quitar_espacios_extremos(input("¿Cuál eliges? (1-4): "))
        if eleccion == "1":
            resultado = "espada"
        elif eleccion == "2":
            resultado = "armadura"
        elif eleccion == "3":
            resultado = "raciones"
        elif eleccion == "4":
            resultado = "bolsa_monedas"
        else:
            print("Opción inválida. Por favor elige 1, 2, 3 o 4.")
    return resultado



def usar_raciones_si_disponible(nombre_usuario: str, es_correcta: bool) -> int:
    """
    Usa las raciones si están disponibles y la respuesta es incorrecta.
    Retorna los puntos recuperados (3 si se usaron las raciones, 0 si no).
    """
    puntos_recuperados = 0
    
    if not es_correcta:
        objeto = verificar_objeto_excepcional(nombre_usuario, ESTADO_BUFF_PATH)
        if objeto == "raciones":
            puntos_recuperados = 3
            print("\n🍖 ¡RACIONES ACTIVADAS! Has recuperado 3 puntos de vida.")
            print("🔧 Consumiendo raciones del inventario...")
            
            # Eliminar las raciones del inventario
            estado = cargar_json(ESTADO_BUFF_PATH, {})
            
            # Buscar el usuario en el estado
            usuario_encontrado = False
            for clave in estado:
                if clave == nombre_usuario:
                    usuario_encontrado = True
                    break
            
            if usuario_encontrado:
                # Buscar "objeto_excepcional" en los datos del usuario
                tiene_objeto_excepcional = False
                for clave in estado[nombre_usuario]:
                    if clave == "objeto_excepcional":
                        tiene_objeto_excepcional = True
                        break
                
                if tiene_objeto_excepcional:
                    del estado[nombre_usuario]["objeto_excepcional"]
                    guardar_json(ESTADO_BUFF_PATH, estado)
    
    resultado_final = puntos_recuperados
    return resultado_final



def usar_bolsa_monedas_si_disponible(nombre_usuario: str, es_correcta: bool, puntos_base: int) -> int:
    """
    Usa la bolsa de monedas si está disponible y la respuesta es correcta.
    Retorna los puntos extra (igual a puntos_base si se usó, 0 si no).
    """
    puntos_extra = 0
    if es_correcta:
        objeto = verificar_objeto_excepcional(nombre_usuario, ESTADO_BUFF_PATH)
        if objeto == "bolsa_monedas":
            puntos_extra = puntos_base
            print(f"\n💰 ¡BOLSA DE MONEDAS ACTIVADA! Has duplicado tus puntos: +{puntos_extra}")
            print("🔧 Consumiendo bolsa de monedas del inventario...")
            # Eliminar la bolsa de monedas del inventario
            estado = cargar_json(ESTADO_BUFF_PATH, {})
            
            # Verificar si el usuario existe en el estado
            usuario_existe = False
            for usuario in estado:
                if usuario == nombre_usuario:
                    usuario_existe = True
                    break
            
            if usuario_existe:
                # Verificar si tiene objeto_excepcional
                objeto_excepcional_existe = False
                for clave in estado[nombre_usuario]:
                    if clave == "objeto_excepcional":
                        objeto_excepcional_existe = True
                        break
                
                if objeto_excepcional_existe:
                    # Crear nuevo diccionario sin objeto_excepcional
                    nuevo_usuario_estado = {}
                    for clave in estado[nombre_usuario]:
                        if clave != "objeto_excepcional":
                            nuevo_usuario_estado[clave] = estado[nombre_usuario][clave]
                    estado[nombre_usuario] = nuevo_usuario_estado
                    guardar_json(ESTADO_BUFF_PATH, estado)
    return puntos_extra



def mostrar_objeto_obtenido(objeto_elegido: str) -> None:
    """Muestra el mensaje correspondiente según el objeto elegido"""
    if objeto_elegido == "espada":
        print("⚔️ ¡Has obtenido la ESPADA DE LA ESFINGE!")
        print("   • +2 puntos extra por respuesta correcta")
        print("   • Un reintento especial disponible")
    elif objeto_elegido == "armadura":
        print("🛡️ ¡Has obtenido la ARMADURA DE LA ESFINGE!")
        print("   • Protección automática contra una respuesta incorrecta")
    elif objeto_elegido == "raciones":
        print("🍖 ¡Has obtenido las RACIONES DE LA ESFINGE!")
        print("   • Recupera 3 puntos de vida cuando falles una pregunta")
    elif objeto_elegido == "bolsa_monedas":
        print("💰 ¡Has obtenido la BOLSA DE MONEDAS DE LA ESFINGE!")
        print("   • Duplica los puntos de la última pregunta correcta")

ESTADO_BUFF_PATH = "EstadoBuff.json"



def guardar_objeto_excepcional(nombre_usuario: str, objeto: str, estado_path: str) -> None:
    estado = cargar_json(estado_path, {})

    existe = False
    for usuario in estado:
        if usuario == nombre_usuario:
            existe = True
            break

    if not existe:
        estado[nombre_usuario] = {}

    estado[nombre_usuario]["objeto_excepcional"] = objeto
    guardar_json(estado_path, estado)
    return None


def verificar_objeto_excepcional(nombre_usuario: str, estado_path: str) -> None:
    resultado = None
    if verificar_archivo_existe(estado_path, ""):
        estado = cargar_json(estado_path)
        
        # Verificar si el usuario existe en el estado
        usuario_existe = False
        for usuario in estado:
            if usuario == nombre_usuario:
                usuario_existe = True
                break
        
        if usuario_existe:
            # Verificar si tiene objeto_excepcional
            objeto_excepcional_existe = False
            for clave in estado[nombre_usuario]:
                if clave == "objeto_excepcional":
                    objeto_excepcional_existe = True
                    break
            
            if objeto_excepcional_existe:
                resultado = estado[nombre_usuario]["objeto_excepcional"]
    
    return resultado

def verificar_y_otorgar_objeto_excepcional(nombre_usuario: str, respuestas_correctas: int, total_preguntas: int) -> None:
    if respuestas_correctas >= 8 and total_preguntas == 10:
        objeto_actual = verificar_objeto_excepcional(nombre_usuario, ESTADO_BUFF_PATH)
        if objeto_actual is None:
            print("\n🌟 ¡FELICIDADES! Has logrado un rendimiento excepcional.")
            objeto_elegido = preguntar_espada_armadura()
            guardar_objeto_excepcional(nombre_usuario, objeto_elegido, ESTADO_BUFF_PATH)
            if objeto_elegido == "espada":
                print("⚔️ ¡Has obtenido la ESPADA DE LA ESFINGE!")
                print("   • +2 puntos extra por respuesta correcta")
                print("   • Un reintento especial disponible")
            else:
                print("🛡️ ¡Has obtenido la ARMADURA DE LA ESFINGE!")
                print("   • Protección automática contra una respuesta incorrecta")



def usar_armadura_si_disponible(nombre_usuario: str, es_correcta: bool) -> bool:
    resultado = False
    
    if not es_correcta:
        objeto = verificar_objeto_excepcional(nombre_usuario, ESTADO_BUFF_PATH)
        if objeto == "armadura":
            print("\n🛡️ ¡ARMADURA ACTIVADA! Tu respuesta incorrecta ha sido protegida.")
            print("🔧 Eliminando armadura del inventario...")
            estado = cargar_json(ESTADO_BUFF_PATH, {})
            
            # Verificar si el usuario existe en el estado
            usuario_existe = False
            for usuario in estado:
                if usuario == nombre_usuario:
                    usuario_existe = True
                    break
            
            if usuario_existe:
                # Verificar si tiene objeto_excepcional
                objeto_excepcional_existe = False
                for clave in estado[nombre_usuario]:
                    if clave == "objeto_excepcional":
                        objeto_excepcional_existe = True
                        break
                
                if objeto_excepcional_existe:
                    # Crear nuevo diccionario sin objeto_excepcional
                    nuevo_usuario_estado = {}
                    for clave in estado[nombre_usuario]:
                        if clave != "objeto_excepcional":
                            nuevo_usuario_estado[clave] = estado[nombre_usuario][clave]
                    estado[nombre_usuario] = nuevo_usuario_estado
                    guardar_json(ESTADO_BUFF_PATH, estado)
            resultado = True
    
    return resultado