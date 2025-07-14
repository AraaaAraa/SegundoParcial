import random

def generar_matriz_resoluble(tamano: int) -> list:
    matriz = inicializar_matriz_vacia(tamano)
    camino = generar_camino_garantizado(tamano)
    asignar_valores_a_camino(matriz, camino)
    rellenar_matriz_con_valores_seguro(matriz, camino)
    matriz_final = matriz
    return matriz_final

def inicializar_matriz_vacia(tamano: int) -> list:
    matriz = []
    fila_idx = 0
    while fila_idx < tamano:
        fila = []
        col_idx = 0
        while col_idx < tamano:
            fila.append(0)
            col_idx += 1
        matriz.append(fila)
        fila_idx += 1
    return matriz

def generar_camino_garantizado(tamano: int, fila=0, col=0, camino=[]) -> list:
    
    if not camino:  
        camino = []
    
    camino.append((fila, col))
    
    if (fila, col) == (tamano - 1, tamano - 1):
        return camino
    opciones = []
    if fila + 1 < tamano:
        opciones.append((fila + 1, col))
    if col + 1 < tamano:
        opciones.append((fila, col + 1))
    if fila + 1 < tamano and col + 1 < tamano:
        opciones.append((fila + 1, col + 1))
    
    nueva_fila, nueva_col = random.choice(opciones)
    return generar_camino_garantizado(tamano, nueva_fila, nueva_col, camino)

def asignar_valores_a_camino(matriz: list, camino: list):
    import random
    valor = random.randint(10, 20)
    for fila, col in camino:
        matriz[fila][col] = valor
        valor += random.randint(1, 5)

def rellenar_matriz_con_valores_seguro(matriz: list, camino: list):
    import random
    tamano = len(matriz)
    for i in range(tamano):
        for j in range(tamano):
            if (i, j) not in camino:
                vecinos = obtener_valores_vecinos_no_nulos(matriz, i, j)
                if vecinos:
                    min_vecino = min(vecinos)
                    matriz[i][j] = random.randint(10, min_vecino + 10)
                else:
                    matriz[i][j] = random.randint(10, 50)

def obtener_valores_vecinos_no_nulos(matriz: list, fila: int, col: int) -> list:
    tamano = len(matriz)
    vecinos = [
        (fila - 1, col), (fila + 1, col),
        (fila, col - 1), (fila, col + 1),
        (fila - 1, col - 1), (fila - 1, col + 1),
        (fila + 1, col - 1), (fila + 1, col + 1)
    ]

    vecinos_validos = [
        matriz[x][y]
        for x, y in vecinos
        if 0 <= x < tamano and 0 <= y < tamano and matriz[x][y] != 0
    ]
    return vecinos_validos

def mostrar_matriz_con_jugador(matriz: list, jugador_pos: tuple, camino_recorrido: list) -> None:
    """
    Muestra la matriz con la posición del jugador y el camino recorrido.

    Args:
        matriz (list): Matriz de valores enteros.
        jugador_pos (tuple): Posición actual del jugador (i, j).
        camino_recorrido (list): Lista de tuplas con posiciones ya recorridas.
    """
    i = 0
    while i < len(matriz):
        fila = matriz[i]
        linea = ""
        j = 0
        while j < len(fila):
            valor = fila[j]
            if jugador_pos[0] == i and jugador_pos[1] == j:
                linea = linea + f"[{valor:2}]"
            else:
                esta_en_camino = False
                k = 0
                while k < len(camino_recorrido):
                    if camino_recorrido[k][0] == i and camino_recorrido[k][1] == j:
                        esta_en_camino = True
                    k = k + 1
                if esta_en_camino:
                    linea = linea + f" {valor:2}*"
                else:
                    linea = linea + f" {valor:2} "
            linea = linea + " "
            j = j + 1
        print(linea)
        i = i + 1
    print()

def mostrar_movimientos_validos(matriz, pos_actual, valor_actual):
    """Muestra los movimientos válidos desde la posición actual"""
    fila, col = pos_actual
    movimientos = []
    direcciones = [
        (-1, -1, "↖"), (-1, 0, "↑"), (-1, 1, "↗"),
        (0, -1, "←"),                  (0, 1, "→"),
        (1, -1, "↙"),  (1, 0, "↓"),  (1, 1, "↘")
    ]
    
    print("Movimientos válidos:")
    indice_movimiento = 1 # Inicializamos un contador para los movimientos
    for direccion_fila, direccion_columna, simbolo in direcciones:
        nueva_fila, nueva_col = fila + direccion_fila, col + direccion_columna
        if (0 <= nueva_fila < len(matriz) and 
            0 <= nueva_col < len(matriz[0])):
            nuevo_valor = matriz[nueva_fila][nueva_col]
            if nuevo_valor > valor_actual:
                movimientos.append((nueva_fila, nueva_col, indice_movimiento, simbolo))
                print(f"{indice_movimiento}. {simbolo} -> ({nueva_fila},{nueva_col}) [valor: {nuevo_valor}]")
                indice_movimiento += 1 # Incrementamos el contador
    
    return movimientos


def jugar_guardianes():
    print("\n=== GUARDIANES DE PIEDRA ===")
    print("Objetivo: Llegar desde (0,0) hasta la esquina inferior derecha")
    print("Regla: Solo puedes moverte a casillas con valores MAYORES al actual")
    print("Leyenda: [XX] = Tu posición, XX* = Camino recorrido\n")

    tamano = 5
    matriz = generar_matriz_resoluble(tamano)
    print("Matriz con solución garantizada generada!\n")

    jugador_pos = (0, 0)
    objetivo = (tamano - 1, tamano - 1)
    camino = set()
    valor_actual = matriz[0][0]

    print("Matriz de guardianes:")
    mostrar_matriz_con_jugador(matriz, jugador_pos, camino)

    resultado = resolver_guardianes(matriz, jugador_pos, objetivo, valor_actual, camino)
    return resultado

def obtener_movimiento_por_opcion(movimientos, opcion):
    for mov in movimientos:
        if mov[2] == opcion:
            return mov
    return None

def mostrar_mensaje_victoria(pos_final, camino, matriz):
    print("\n🎉 ¡FELICITACIONES! 🎉")
    print("¡Has liberado correctamente a los guardianes!")
    print("Obtienes una mejora especial para tu aventura.")
    camino.add(pos_final)
    print("\nCamino completo recorrido:")
    mostrar_matriz_con_jugador(matriz, (-1, -1), camino)

def resolver_guardianes(matriz, jugador_pos, objetivo, valor_actual, camino):
    resultado = False

    if jugador_pos == objetivo:
        resultado = manejar_victoria(jugador_pos, camino, matriz)
    else:
        mostrar_estado_actual(jugador_pos, valor_actual, objetivo)
        movimientos_validos = mostrar_movimientos_validos(matriz, jugador_pos, valor_actual)

        if not movimientos_validos:
            resultado = manejar_derrota()
        else:
            entrada = pedir_entrada_usuario()
            resultado = procesar_entrada(
                entrada,
                matriz,
                jugador_pos,
                objetivo,
                valor_actual,
                camino,
                movimientos_validos
            )

    return resultado


def manejar_victoria(jugador_pos, camino, matriz):
    mostrar_mensaje_victoria(jugador_pos, camino, matriz)
    return True

def manejar_derrota():
    print("\n¡No hay movimientos válidos! Has quedado atrapado.")
    print("Los guardianes permanecen petrificados...")
    return False

def mostrar_estado_actual(jugador_pos, valor_actual, objetivo):
    print(f"\nPosición actual: {jugador_pos} [valor: {valor_actual}]")
    print(f"Objetivo: {objetivo}")

def pedir_entrada_usuario():
    print("\n¿Qué movimiento eliges? (número del 1-8, 'r' para reiniciar, 'q' para salir)")
    return input("Tu elección: ").strip().lower()

def procesar_entrada(entrada, matriz, jugador_pos, objetivo, valor_actual, camino, movimientos_validos):
    if entrada == 'q':
        print("Saliendo del juego...")
        return False

    if entrada == 'r':
        print("Reiniciando juego...")
        return jugar_guardianes()

    if not entrada.isdigit():
        print("Por favor ingresa un número válido.")
        return resolver_guardianes(matriz, jugador_pos, objetivo, valor_actual, camino)

    opcion = int(entrada)
    movimiento = obtener_movimiento_por_opcion(movimientos_validos, opcion)

    if not movimiento:
        print("Opción no válida. Intenta de nuevo.")
        return resolver_guardianes(matriz, jugador_pos, objetivo, valor_actual, camino)

    return avanzar_y_continuar(matriz, jugador_pos, movimiento, objetivo, camino)

def avanzar_y_continuar(matriz, jugador_pos, movimiento, objetivo, camino):
    camino.add(jugador_pos)
    nueva_pos = (movimiento[0], movimiento[1])
    nuevo_valor = matriz[nueva_pos[0]][nueva_pos[1]]

    print(f"\nTe mueves a {nueva_pos} con valor {nuevo_valor}")
    print("Estado actual:")
    mostrar_matriz_con_jugador(matriz, nueva_pos, camino)

    return resolver_guardianes(matriz, nueva_pos, objetivo, nuevo_valor, camino)