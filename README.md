# 🎯 Juego de Trivia Mitológica

Un juego de trivia interactivo en Python que combina conocimientos de mitología griega, egipcia y hebrea con un sistema de buffeos, objetos especiales y minijuegos.

## 🎮 Características Principales

### 🏆 Sistema de Juego
- **3 Niveles de dificultad** con preguntas de diferentes categorías
- **Sistema de racha** que otorga bonificaciones por respuestas consecutivas correctas
- **Objetos especiales** desbloqueables con efectos únicos
- **Sistema de reintentos** basado en rendimiento
- **Estadísticas detalladas** y ranking de jugadores

### ⚔️ Objetos Especiales de la Esfinge
Los jugadores pueden obtener objetos excepcionales al lograr 8+ respuestas correctas en una partida de 10 preguntas:

- **🗡️ Espada**: +2 puntos extra por respuesta correcta + reintento especial
- **🛡️ Armadura**: Protección automática contra una respuesta incorrecta
- **🍖 Raciones**: Recupera 3 puntos de vida al fallar una pregunta
- **💰 Bolsa de Monedas**: Duplica los puntos de la última pregunta correcta

### 🎲 Minijuego: Guardianes de Piedra
Un juego de estrategia donde debes navegar por una matriz desde (0,0) hasta la esquina inferior derecha, moviéndote solo a casillas con valores mayores.

## 📁 Estructura del Proyecto

```
├── Main.py                      # Punto de entrada principal
├── buffeos.py                   # Sistema de objetos especiales y buffeos
├── generales.py                 # Funciones utilitarias generales
├── manejo_de_usuario.py         # Gestión de usuarios y estadísticas
├── Minijuego.py                 # Juego de Guardianes de Piedra
├── preguntas.py                 # Carga y manejo de preguntas
├── prints_de_juego.py           # Funciones de visualización
├── procesos_recopilatorios.py   # Lógica principal de partidas
├── puntaje.py                   # Sistema de puntuación
├── validaciones_y_prints.py    # Validaciones y procesamiento de respuestas
├── verificacion_archivos.py    # Manejo de archivos JSON/CSV
├── preguntas.csv               # Base de datos de preguntas
├── Usuarios.json               # Estadísticas de usuarios
└── EstadoBuff.json             # Estado de objetos especiales
```

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.x
- No requiere dependencias externas

### Ejecución
```bash
git clone [tu-repositorio]
cd [nombre-del-proyecto]
python Main.py
```

## 🎯 Cómo Jugar

### Menú Principal
1. **Juego Principal**: Inicia una partida completa
2. **Ver Estadísticas**: Muestra tu progreso personal
3. **Ver Ranking**: Tabla de clasificación de todos los jugadores
4. **Minijuego Extra**: Juega Guardianes de Piedra
5. **Salir**: Termina el programa

### Mecánicas de Juego

#### 📈 Sistema de Puntuación
- **Nivel 1**: 1 punto por respuesta correcta, -1 por incorrecta
- **Nivel 2**: 2 puntos por respuesta correcta, -2 por incorrecta  
- **Nivel 3**: 3 puntos por respuesta correcta, -3 por incorrecta

#### 🔥 Sistema de Racha
- **3+ respuestas correctas**: +1 punto extra
- **5+ respuestas correctas**: +3 puntos extra
- **7+ respuestas correctas**: +5 puntos extra

#### 🛡️ Sistema de Reintentos
- Disponible con racha de 2+ respuestas correctas
- Espada otorga reintento especial independiente de la racha
- Máximo 2 errores por partida antes del fin del juego

## 📊 Formatos de Datos

### preguntas.csv
```csv
id,nivel,descripcion,dificultad,categoria,opcion_correcta,opcion1,opcion2,opcion3,opcion4
```

### Usuarios.json
Almacena estadísticas detalladas incluyendo:
- Número de intentos
- Historial de puntajes, tiempos y aciertos
- Porcentajes de éxito
- Historial detallado de respuestas

### EstadoBuff.json
Gestiona el estado de objetos especiales por usuario:
```json
{
  "usuario": {
    "objeto_excepcional": "espada|armadura|raciones|bolsa_monedas"
  }
}
```

## 🎨 Características Técnicas

### 🔧 Arquitectura Modular
- Separación clara de responsabilidades
- Funciones puras sin efectos secundarios
- Manejo robusto de archivos JSON/CSV

### 📝 Implementación Sin Librerías Externas
- Implementaciones propias de funciones como `sum()`, `min()`, `max()`
- Algoritmos de ordenamiento personalizados
- Manejo manual de strings y listas

### 🎯 Características de Código
- Manejo de errores robusto
- Validaciones exhaustivas de entrada
- Persistencia de datos en archivos locales
- Sistema de logging implícito en las estadísticas

## 🎲 Minijuego: Guardianes de Piedra

Un puzzle estratégico donde:
- Comienzas en la esquina superior izquierda (0,0)
- Objetivo: llegar a la esquina inferior derecha
- Regla: solo puedes moverte a casillas con valores **mayores** al actual
- Genera matrices con solución garantizada usando algoritmos recursivos

### Controles
- **1-8**: Seleccionar movimiento direccional
- **r**: Reiniciar partida
- **q**: Salir del minijuego

## 🏆 Sistema de Progresión

1. **Juega partidas** para acumular estadísticas
2. **Mantén rachas** para obtener bonificaciones
3. **Logra 8+ aciertos** en partidas de 10 preguntas para desbloquear objetos
4. **Usa objetos estratégicamente** para maximizar puntuación
5. **Compite en el ranking** con otros jugadores

## 📈 Estadísticas Disponibles

- Promedio de puntajes y porcentajes de acierto
- Mejor puntaje y mejor porcentaje histórico
- Tiempos promedio y mejor tiempo
- Número total de partidas jugadas
- Historial completo de respuestas

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Agregar nuevas preguntas al archivo CSV
- Implementar nuevos tipos de objetos especiales
- Crear minijuegos adicionales
- Mejorar la interfaz de usuario
- Optimizar algoritmos existentes

## 📋 Próximas Características

- [ ] Modo multijugador
- [ ] Categorías de preguntas personalizables
- [ ] Sistema de logros
- [ ] Exportación de estadísticas
- [ ] Interfaz gráfica

## 📄 Licencia

[Especifica tu licencia aquí]

## 👨‍💻 Autor

[Tu nombre/usuario de GitHub]

---

*¡Que la sabiduría de la Esfinge te acompañe en tu aventura!* 🦅
