# PROYECTO FINAL - INTRODUCCIÓN A LOS VIDEOJUEGOS

Bienvenido al proyecto de desarrollo de un videojuego implementado en Python. Para este proyecto, se utilizó el patrón de diseño Entity-Component-Systems (ECS), una decisión motivada tanto por las restricciones del proyecto como por la necesidad de facilitar la interacción entre los diferentes elementos del juego.

Este proyecto representa un esfuerzo colaborativo para crear un videojuego robusto y fácilmente mantenible. Esperamos que encuentres útil y educativo explorar nuestro código y diseño. ¡Gracias por visitar nuestro repositorio y por tu interés en nuestro proyecto!

## Integrantes del equipo
- **[Felipe Cerquera](https://github.com/orgs/Miso-Code/people/pipeCer)**
- **[Erik Fernando Loaiza Patiño](https://github.com/orgs/Miso-Code/people/erikloaiza)**
- **[Brayan Henao](https://github.com/orgs/Miso-Code/people/brayanhenao)**
- **[Rodrigo Escobar Lopez](https://github.com/orgs/Miso-Code/people/ocralo)**

## Descripción del juego
El juego que estamos desarrollando es un juego de plataformas en 2D. El jugador controla a un personaje que debe eliminar y esquivar diferentes enemigos para superar los diferentes niveles. El juego cuenta con un sistema de puntuación y un sistema de vidas, que se reducen cada vez que el jugador es golpeado por un enemigo o una bala.

## Estructura del proyecto
El proyecto está organizado de la siguiente manera:
- **`assets/`**: Carpeta que contiene los recursos del juego, como imágenes, sonidos y fuentes.
- **`esper/`**: Carpeta que contiene el código fuente de la librería `esper`, que implementa el patrón de diseño ECS.
- **`src/`**: Carpeta que contiene el código fuente del juego.
  - **`create`**: Módulo que contiene funciones para crear entidades y componentes.
  - **`ecs`**: Módulo que contiene las clases y funciones necesarias para implementar el patrón ECS.
  - **`engine`**: Módulo que contiene las clases y funciones necesarias para implementar el motor del juego.
- **`README.md`**: Archivo que contiene la información general del proyecto.
- **`requirements.txt`**: Archivo que contiene las dependencias del proyecto.
- **`main.py`**: Archivo que contiene el punto de entrada del juego.
- **`.gitignore`**: Archivo que contiene los archivos y carpetas que se deben ignorar en el control de versiones.
- **`.pre-commit-config.yaml`**: Archivo de configuración de `pre-commit`.

## Requerimientos
Para ejecutar el juego, necesitas tener instalado Python 3.7 o superior.

## Inicialización
Para inicializar el proyecto, sigue los siguientes pasos:
1. Clona el repositorio en tu máquina local.
2. Crea un entorno virtual en la raíz del proyecto:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
4. Instala las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Para ejecutar el juego, sigue los siguientes pasos:
1. Activa el entorno virtual:
   1. En Windows:
      ```bash
      venv\Scripts\activate
      ```
    2. En Linux o macOS:
        ```bash
        source venv/bin/activate
        ```

2. Ejecuta el archivo `main.py`:
   ```bash
   python main.py
   ```

## Despliegue
Para ver el juego en acción, visita el siguiente enlace: [Juego de Invaders](https://misoteam.itch.io/invaders)
