**-ESPAÑOL-**

📜 **Juego de Trivia Mitológica**
Este proyecto simula un juego de trivia interactivo con temáticas de mitología griega, egipcia y hebrea. Incluye un sistema de buffs, objetos especiales, minijuegos y estadísticas avanzadas para los jugadores.

🛠️ **Tecnologías Utilizadas**

* Python 3
* Estructuras de datos básicas (listas, bucles, condicionales)
* Programación modular
* Uso de archivos CSV y JSON para persistencia
* Algoritmos personalizados (ordenamiento, recorridos en matriz)
* Separación en módulos (import, organización en archivos `.py`)

📁 **Estructura de Carpetas**

```
├── Main.py                    # Menú principal del programa (interfaz de usuario)
├── buffeos.py                 # Sistema de objetos especiales y buffs
├── generales.py               # Funciones utilitarias generales
├── manejo_de_usuario.py       # Gestión de usuarios y estadísticas
├── Minijuego.py               # Minijuego "Guardianes de Piedra"
├── preguntas.py               # Manejo y carga de preguntas desde CSV
├── prints_de_juego.py         # Visualización e interfaces gráficas por consola
├── procesos_recopilatorios.py # Lógica principal de partidas
├── puntaje.py                 # Sistema de puntuación y rachas
├── validaciones_y_prints.py   # Validaciones y procesamiento de respuestas
├── verificacion_archivos.py   # Gestión de archivos JSON y CSV
├── preguntas.csv              # Base de datos de preguntas
├── Usuarios.json              # Registro de estadísticas por jugador
└── EstadoBuff.json            # Estado de objetos especiales por usuario
```

📌 **Ejercicios Desarrollados**

* Registro de usuarios y control de intentos por partida
* Sistema de trivia con 3 niveles de dificultad
* Bonificaciones por racha de respuestas correctas
* Desbloqueo de objetos especiales (espada, armadura, raciones, bolsa de monedas)
* Submenú con estadísticas detalladas del jugador
* Minijuego con lógica recursiva: Guardianes de Piedra
* Rankings globales y almacenamiento de partidas
* Validación de respuestas, puntuación y reintentos estratégicos

🧠 **Habilidades Desarrolladas**

* Pensamiento lógico y estructuras de control avanzadas
* Modularización de código y separación de responsabilidades
* Manipulación de archivos `.json` y `.csv`
* Algoritmos de recorrido en matrices y ordenamiento personalizado
* Validación exhaustiva de entrada del usuario
* Persistencia de datos y análisis estadístico
* Diseño de minijuegos con restricciones lógicas (valores crecientes en matriz)

▶️ **¿Cómo Ejecutarlo?**

1. Asegurate de tener **Python 3.10 o superior** instalado.
2. Descargá todos los archivos `.py`, `.csv` y `.json` en la misma carpeta.
3. Abrí una terminal o consola en esa carpeta.
4. Ejecutá el programa principal con:

   ```bash
   python Main.py
   ```
5. Seguí las instrucciones del menú para jugar, consultar estadísticas, revisar el ranking o acceder al minijuego.

💡 **Notas**

* Las preguntas se leen desde el archivo `preguntas.csv`.
* Las estadísticas se guardan automáticamente en `Usuarios.json`.
* Solo se desbloquean objetos si se logran **8 o más aciertos** en una partida de 10 preguntas.
* El minijuego **Guardianes de Piedra** genera matrices con solución garantizada y permite reinicios.
* El programa no utiliza librerías externas (todo está implementado con Python puro).

**-ENGLISH-**

📜 **Mythological Trivia Game**
This project simulates an interactive trivia game focused on Greek, Egyptian, and Hebrew mythology. It includes a buff system, unlockable special items, minigames, and detailed player statistics.

🛠️ **Technologies Used**

* Python 3
* Basic data structures (lists, loops, conditionals)
* Modular programming
* CSV and JSON file handling
* Custom algorithms (sorting, matrix traversal)
* Separation into modules (`import`, organized `.py` files)

📁 **Folder Structure**

```
├── Main.py                    # Main menu (user interface)
├── buffeos.py                 # Special item and buff system
├── generales.py               # General utility functions
├── manejo_de_usuario.py       # User management and statistics
├── Minijuego.py               # "Stone Guardians" minigame
├── preguntas.py               # Loading and handling trivia questions
├── prints_de_juego.py         # Display and interface functions
├── procesos_recopilatorios.py # Main game logic
├── puntaje.py                 # Scoring and streak system
├── validaciones_y_prints.py   # Input validation and response processing
├── verificacion_archivos.py   # JSON and CSV file handling
├── preguntas.csv              # Question database
├── Usuarios.json              # Player statistics
└── EstadoBuff.json            # User-specific special item tracking
```

📌 **Implemented Features**

* User registration and session tracking
* Trivia gameplay with 3 levels of difficulty
* Bonus points for consecutive correct answers
* Unlockable items (sword, armor, rations, coin bag)
* Statistics submenu showing personal performance
* Recursive logic minigame: *Stone Guardians*
* Global ranking system and persistent session data
* Validation of user input, scoring, and retry logic

🧠 **Skills Developed**

* Logical thinking and advanced control structures
* Modularized code and file responsibility separation
* Manipulation of `.json` and `.csv` files
* Custom matrix traversal and sorting algorithms
* Strict user input validation
* Data persistence and statistical analysis
* Minigame design with logical constraints (only move to higher values)

▶️ **How to Run It**

1. Make sure you have **Python 3.10 or higher** installed.
2. Download all `.py`, `.csv`, and `.json` files into the same folder.
3. Open a terminal or command prompt in that folder.
4. Run the main script with:

   ```bash
   python Main.py
   ```
5. Follow the on-screen instructions to start the game, view statistics, check rankings, or access the minigame.

💡 **Notes**

* Questions are loaded from the `preguntas.csv` file.
* Player data is saved automatically in `Usuarios.json`.
* Special items are only unlocked by scoring **8 or more correct answers** in a 10-question game.
* The *Stone Guardians* minigame generates solvable matrices with guaranteed paths and restart options.
* The project uses no external libraries — all logic is implemented with pure Python.
