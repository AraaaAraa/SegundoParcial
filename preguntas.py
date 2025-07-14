import random
from verificacion_archivos import verificar_archivo_y_devolver_path
from typing import Dict, List



def mezclar_opciones(opciones: list) -> list:
    mezcladas = opciones[:]
    i = len(mezcladas) - 1
    while i > 0:
        j = random.randint(0, i)
        temp = mezcladas[i]
        mezcladas[i] = mezcladas[j]
        mezcladas[j] = temp
        i = i - 1
    return mezcladas




def procesar_linea_csv(fila: list) -> dict:
    try:
        pid = int(fila[0])
        nivel = int(fila[1])
        descripcion = fila[2].strip('"')
        dificultad = int(fila[3])
        categoria = fila[4]
        opcion_correcta = int(fila[5])
        opciones = (fila[6], fila[7], fila[8], fila[9])
        if 1 <= opcion_correcta <= 4:
            respuesta_correcta = opciones[opcion_correcta - 1]
        else:
            respuesta_correcta = opciones[0]
        opciones_mezcladas = mezclar_opciones(list(opciones))
        pregunta = {
            "id": pid,
            "nivel": nivel,
            "descripcion": descripcion,
            "dificultad": dificultad,
            "categoria": categoria,
            "opciones": opciones_mezcladas,
            "correcta": respuesta_correcta
        }
        return pregunta
    except Exception:
        return {}




def cargar_preguntas_con_opciones(path: str) -> dict:
    preguntas = {}
    abs_path = verificar_archivo_y_devolver_path(path)
    if abs_path != "":
        with open(abs_path, encoding="utf-8") as f:
            encabezado = f.readline()
            for linea in f:
                fila = linea.strip().split(",")
                if len(fila) >= 10:
                    pregunta = procesar_linea_csv(fila)
                    if "id" in pregunta:
                        preguntas[pregunta["id"]] = {
                            "nivel": pregunta["nivel"],
                            "descripcion": pregunta["descripcion"],
                            "dificultad": pregunta["dificultad"],
                            "categoria": pregunta["categoria"],
                            "opciones": pregunta["opciones"],
                            "correcta": pregunta["correcta"]
                        }
    return preguntas



def filtrar_preguntas_por_nivel(
    pids: List[int],
    preguntas: Dict[int, Dict],
    nivel: int,
    resultado: Dict[int, Dict]
) -> Dict[int, Dict]:
    if not pids:
        return resultado

    pid_actual = pids[0]
    pregunta_actual = preguntas[pid_actual]

    if pregunta_actual['nivel'] == nivel:
        resultado[pid_actual] = pregunta_actual

    return filtrar_preguntas_por_nivel(pids[1:], preguntas, nivel, resultado)



def seleccionar_pregunta(preguntas: Dict[int, Dict], nivel: int) -> Dict:
    preguntas_nivel = filtrar_preguntas_por_nivel(preguntas, nivel)
    if not preguntas_nivel:
        print(f"❌ No hay preguntas de nivel {nivel}")
        return {}

    categorias = []
    for p in preguntas_nivel.values():
        repetida = False
        for c in categorias:
            if c == p['categoria']:
                repetida = True
                break
        if not repetida:
            categorias.append(p['categoria'])

    categoria = random.choice(categorias)

    candidatas = []
    for pid, p in preguntas_nivel.items():
        if p['categoria'] == categoria:
            candidatas.append(pid)

    id_pregunta = random.choice(candidatas)

    dicc = {"id": id_pregunta}
    for k in preguntas[id_pregunta]:
        dicc[k] = preguntas[id_pregunta][k]

    return dicc




def seleccionar_pregunta_de_disponibles(preguntas_disponibles: Dict[int, Dict]) -> Dict:
    if not preguntas_disponibles:
        return {}

    categorias = []
    for p in preguntas_disponibles.values():
        ya_esta = False
        for c in categorias:
            if c == p['categoria']:
                ya_esta = True
                break
        if not ya_esta:
            categorias.append(p['categoria'])

    categoria = random.choice(categorias)

    candidatas = []
    for pid, p in preguntas_disponibles.items():
        if p['categoria'] == categoria:
            candidatas.append(pid)

    id_pregunta = random.choice(candidatas)

    dicc = {"id": id_pregunta}
    for k in preguntas_disponibles[id_pregunta]:
        dicc[k] = preguntas_disponibles[id_pregunta][k]

    return dicc



def filtrar_preguntas_disponibles(preguntas: dict, nivel: int, preguntas_usadas: list) -> dict:
    disponibles = {}
    for pid, pregunta in preguntas.items():
        esta_usada = False
        for usada in preguntas_usadas:
            if usada == pid:
                esta_usada = True
                break

        if pregunta['nivel'] == nivel and not esta_usada:
            disponibles[pid] = pregunta

    return disponibles