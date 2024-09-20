import pygame
import sys
from code.main import Game

# Configuración de la ventana
WIDTH, HEIGHT = 900, 90
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulación con Interfaz')
clock = pygame.time.Clock()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Función para dibujar el layout de la interfaz
def draw_interface():
    # Dibuja el marco exterior
    pygame.draw.rect(screen, GRAY, (50, 50, 700, 500), 5)

    # Sección de subir texto
    pygame.draw.rect(screen, WHITE, (60, 60, 200, 40))  # Cuadro de texto
    pygame.draw.rect(screen, GRAY, (60, 60, 200, 40), 2)  # Borde del cuadro de texto

    # Botones de soluciones
    pygame.draw.rect(screen, WHITE, (60, 120, 150, 40))  # Botón de solución 1
    pygame.draw.rect(screen, WHITE, (60, 180, 150, 40))  # Botón de solución 2
    pygame.draw.rect(screen, WHITE, (60, 240, 150, 40))  # Botón de solución 3
    pygame.draw.rect(screen, GRAY, (60, 120, 150, 40), 2)  # Borde de los botones

    # Área de simulación
    pygame.draw.rect(screen, WHITE, (300, 120, 400, 320))  # Área de la simulación
    pygame.draw.rect(screen, GRAY, (300, 120, 400, 320), 2)  # Borde del área

    # Botón de iniciar
    pygame.draw.rect(screen, WHITE, (300, 460, 100, 40))  # Botón de iniciar
    pygame.draw.rect(screen, GRAY, (300, 460, 100, 40), 2)  # Borde del botón

# Simulación de ejemplo
def run_simulation():
	game = Game()
	game.run()

def main():
    running = True
    while running:
        screen.fill(WHITE)  # Fondo blanco
        
        # Dibuja la interfaz
        draw_interface()

        # Dibujar la simulación
        run_simulation()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
