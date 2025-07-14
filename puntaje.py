from buffeos import aplicar_buffeo_en_partida, usar_raciones_si_disponible, usar_bolsa_monedas_si_disponible



def calcular_puntos_base(es_correcta: bool, dificultad: int) -> int:
    var = dificultad if es_correcta else -dificultad
    return var



def calcular_puntaje_total(
    es_correcta: bool,
    dificultad: int,
    racha_actual: int,
    nombre_usuario: str
) -> dict:
    puntos_base = calcular_puntos_base(es_correcta, dificultad)
    puntos_buffeo = aplicar_buffeo_en_partida(es_correcta, "puntos_extra", racha_actual, nombre_usuario)
    puntos_raciones = usar_raciones_si_disponible(nombre_usuario, es_correcta)
    puntos_bolsa = usar_bolsa_monedas_si_disponible(nombre_usuario, es_correcta, puntos_base)

    total = puntos_base + puntos_buffeo + puntos_raciones + puntos_bolsa

    resultado = {
        "total": total,
        "base": puntos_base,
        "buffeo": puntos_buffeo
    }

    return resultado