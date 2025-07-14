def mi_sum(lista) -> None:
    total = 0
    for valor in lista:
        total = total + valor
    return total

def mi_min(lista) -> None:
    if not lista:
        return 0
    minimo = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] < minimo:
            minimo = lista[i]
        i = i + 1
    return minimo



def mi_max(lista) -> None:
    if not lista:
        return 0
    maximo = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] > maximo:
            maximo = lista[i]
        i = i + 1
    return maximo



def mi_enumerate(lista, inicio=0) -> None:
    res = []
    for j in range(len(lista)):
        res.append((inicio + j, lista[j]))
    return res



def quitar_espacios_extremos(texto) -> None:
    inicio = 0
    final = len(texto) - 1
    while inicio <= final and texto[inicio] == " ":
        inicio = inicio + 1
    while final >= inicio and texto[final] == " ":
        final = final - 1
    resultado = ""
    i = inicio
    while i <= final:
        resultado = resultado + texto[i]
        i = i + 1
    return resultado



def convertir_a_mayusculas(texto) -> None:
    minusculas = "abcdefghijklmnopqrstuvwxyzáéíóúüñ"
    mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ"
    resultado = ""
    i = 0
    while i < len(texto):
        letra = texto[i]
        j = 0
        convertido = False
        while j < len(minusculas):
            if letra == minusculas[j]:
                resultado = resultado + mayusculas[j]
                convertido = True
                break
            j = j + 1
        if not convertido:
            resultado = resultado + letra
        i = i + 1
    return resultado



def encontrar_indice(elemento, lista) -> None:
    i = 0
    while i < len(lista):
        if elemento == lista[i]:
            return i
        i = i + 1
    return -1



def obtener_indice_letra(letra: str) -> int:
    letras = "ABCD"
    i = 0
    while i < len(letras):
        if letra == letras[i]:
            return i
        i = i + 1
    return -1



def calcular_estadisticas_lista(lista) -> None:
    if not lista:
        return {
            "promedio": 0,
            "mejor": 0,
            "peor": 0,
            "total": 0
        }
    total = mi_sum(lista)
    promedio = total / len(lista)
    mejor = mi_max(lista)
    peor = mi_min(lista)
    return {
        "promedio": promedio,
        "mejor": mejor,
        "peor": peor,
        "total": total
    }
