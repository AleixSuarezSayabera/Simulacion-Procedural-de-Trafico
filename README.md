# Generación aleatoria de carreteras infinitas

Una simulación de conducción y generación procedimental de carreteras en 2D desarrollada en Python. Este proyecto destaca por utilizar conceptos de ingeniería civil para el trazado de vías y un sistema dinámico de tráfico.

## Características Principales

* **Generación de Vías Realistas:** El sistema no utiliza giros simples; implementa **Clotoides** (espirales de Euler) para realizar transiciones suaves entre tramos rectos y curvas circulares (Círculos Osculadores).
* **Simulación de Tráfico:** Los vehículos enemigos se generan siguiendo una **Distribución de Poisson**, donde el parámetro $\lambda$ define la densidad del tráfico.
* **Modos de Funcionamiento:**
    * **Modo Juego:** Conducción activa donde debes esquivar el tráfico, gestionar vidas y aumentar tu puntuación.
    * **Modo Crear:** Una herramienta de depuración para generar tramos manualmente, eliminar secciones y explorar el mapa con una cámara libre.
* **Cámara Dinámica:** Implementación de un sistema `WorldView` que gestiona la rotación del mundo respecto al jugador y la transformación de coordenadas de simulación a píxeles de pantalla.

---

## Arquitectura del Proyecto

El código se organiza en módulos especializados:

### Motor Geométrico (`carretera/`)
* **`Clotoide.py`**: Calcula la curva de transición donde la curvatura varía linealmente según la distancia recorrida ($s^2 = 2A^2 \theta$).
* **`Osculador.py`**: Gestiona los tramos de curvatura constante (el "centro" de los giros).
* **`Gir.py`**: Orquestador que combina `Clotoide` -> `Osculador` -> `Clotoide` para crear un giro completo y seguro.
* **`Tram.py`**: La unidad básica que define la geometría, límites y los vehículos presentes en un segmento.

### Entidades (`coche/`)
* **`Cotxe.py`**: Define el comportamiento base de los vehículos, su movimiento y cambios de carril.
* **`Jugador.py`**: Extensión con controles de teclado, gestión de colisiones y sistema de progresión.

### Lógica y Vista (`juego/` & `worldview/`)
* **`Joc.py`**: Bucle principal del modo carrera.
* **`ModeCrear.py`**: Lógica para el modo de edición y visualización técnica.
* **`WorldView.py`**: Sistema de proyección y rotación de cámara.

---

## Compilación

python animacio.py
