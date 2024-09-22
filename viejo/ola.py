import pygame
import time

# Inicializar Pygame
pygame.init()

# Colores
SQUARE_COLOR = (255, 0, 0)
ARROW_COLOR = (0, 0, 255)

# Tamaños
CASILLA_SIZE = 64
CUADRADO_SIZE = 32
FLECHA_ANCHO = 16
FLECHA_ALTO_VERTICAL = 64
FLECHA_ALTO_HORIZONTAL = 64

# Inicializar pantalla
screen = pygame.display.set_mode((400, 400))

# Función para calcular la posición central del cuadrado
def centrar_en_casilla(coordenadas):
    x, y = coordenadas
    transformacion = (x * CASILLA_SIZE, y * CASILLA_SIZE)
    centro = (transformacion[0] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2,
              transformacion[1] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2)
    return centro

# Función para calcular la posición de la flecha
def calcular_posicion_flecha(centro, direccion, tamano_flecha):
    if direccion == "arriba":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] - tamano_flecha)
    elif direccion == "abajo":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] + CUADRADO_SIZE)
    elif direccion == "izquierda":
        return (centro[0] - tamano_flecha, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)
    elif direccion == "derecha":
        return (centro[0] + CUADRADO_SIZE, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)

# Función para obtener el tamaño de la flecha según su crecimiento
def obtener_tamano_flecha(direccion, progreso):
    if direccion == "arriba" or direccion == "abajo":
        return (FLECHA_ANCHO, int(FLECHA_ALTO_VERTICAL * progreso))
    elif direccion == "izquierda" or direccion == "derecha":
        return (int(FLECHA_ALTO_HORIZONTAL * progreso), FLECHA_ANCHO)

# Función para animar la flecha
def animar_flecha(direccion, centro, duracion):
    inicio = time.time()
    progreso = 0

    while progreso < 1:
        screen.fill((255, 255, 255))  # Limpiar pantalla

        # Dibujar el cuadrado rojo en el centro
        pygame.draw.rect(screen, SQUARE_COLOR, pygame.Rect(centro[0], centro[1], CUADRADO_SIZE, CUADRADO_SIZE))

        # Calcular el progreso en función del tiempo transcurrido
        progreso = min(1, (time.time() - inicio) / duracion)

        # Calcular el tamaño de la flecha en función del progreso
        tamano_flecha = obtener_tamano_flecha(direccion, progreso)

        # Obtener la posición de la flecha en función de su tamaño
        centro_flecha = calcular_posicion_flecha(centro, direccion, tamano_flecha[1] if direccion in ["arriba", "abajo"] else tamano_flecha[0])

        # Dibujar la flecha (rectángulo azul) en la posición correcta
        pygame.draw.rect(screen, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad de la animación
        pygame.time.delay(16)  # Aproximadamente 60 FPS

# Ejecutar el juego
running = True
inicio = (2, 0)
centro = centrar_en_casilla(inicio)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Llamar a la función de animación para cada dirección
    animar_flecha("arriba", centro, 1)  # Animación de 1 segundo hacia arriba
    animar_flecha("derecha", centro, 1)  # Animación de 1 segundo hacia la derecha

# Cerrar Pygame
pygame.quit()
