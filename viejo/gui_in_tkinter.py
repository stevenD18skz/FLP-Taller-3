import pygame
import tkinter as tk
from threading import Thread
import queue
import time

# Configuraciones para Pygame
WIDTH, HEIGHT = 600, 400
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Clase que manejará el movimiento del cuadro en Pygame
class PygameWindow:
    def __init__(self, command_queue):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Window")
        self.clock = pygame.time.Clock()
        self.rect_x = 50
        self.rect_y = 50
        self.rect_size = 50
        self.running = True
        self.command_queue = command_queue

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Verifica si se recibió algún comando de Tkinter para mover el cuadro
            try:
                command = self.command_queue.get_nowait()
                if command == "move_right":
                    self.rect_x += 10
            except queue.Empty:
                pass
            
            # Dibujar el cuadro rojo
            self.screen.fill(WHITE)
            pygame.draw.rect(self.screen, RED, (self.rect_x, self.rect_y, self.rect_size, self.rect_size))
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

# Clase que manejará la ventana de Tkinter
class TkinterWindow:
    def __init__(self, command_queue):
        self.root = tk.Tk()
        self.root.title("Tkinter Window")
        self.command_queue = command_queue

        # Botón en Tkinter que enviará el comando de mover el cuadro
        self.move_button = tk.Button(self.root, text="Mover a la derecha", command=self.move_rect)
        self.move_button.pack(pady=20)

    def move_rect(self):
        # Envía el comando de mover a la derecha a la cola de comandos
        self.command_queue.put("move_right")

    def run(self):
        self.root.mainloop()

# Función para iniciar la ventana de Pygame en un hilo separado
def run_pygame_window(command_queue):
    pygame_window = PygameWindow(command_queue)
    pygame_window.run()

# Función principal
if __name__ == "__main__":
    command_queue = queue.Queue()  # Cola para enviar comandos entre Tkinter y Pygame

    # Iniciar Pygame en un hilo separado
    pygame_thread = Thread(target=run_pygame_window, args=(command_queue,))
    pygame_thread.start()

    # Iniciar la ventana de Tkinter en el hilo principal
    tkinter_window = TkinterWindow(command_queue)
    tkinter_window.run()

    # Esperar a que termine el hilo de Pygame
    pygame_thread.join()
