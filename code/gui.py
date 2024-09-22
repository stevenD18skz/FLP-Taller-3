import pygame
import sys
from settings import *
from level import Level
from tkinter import Label, Tk, filedialog
from tkinter import Button as bt
import threading
import time
from support import *

# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
BORDER_COLOR = (0, 0, 0)  # Color del borde

class TreeDisplay:
    def __init__(self, x, y, width, height, font_size=18, text_color=BLACK, bg_color=WHITE, border_color=BORDER_COLOR, border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.text_lines = []

    def update_tree(self, tree_text):
        self.text_lines = tree_text.splitlines()

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        y_offset = 10
        for line in self.text_lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += text_surface.get_height() + 5

class Button:
    def __init__(self, text, x, y, width, height, font_size=36, color=LIGHT_GRAY, border_color=BORDER_COLOR, border_width=2):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.font = pygame.font.Font(None, font_size)
        self.active = True

    def draw(self, surface):
        button_color = self.color if self.active else DARK_GRAY
        pygame.draw.rect(surface, button_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('POKEMON')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.algorithm_choice = 'No informada'
        self.buttons = [Button('No informada', 650, 40, 150, 40, font_size=24, color=LIGHT_GRAY),
                        Button('Informada', 810, 40, 150, 40, font_size=24, color=LIGHT_GRAY),
                        Button('Subir archivo', 800, 580, 150, 40, font_size=24, color=LIGHT_GRAY)]
        self.tree_display = TreeDisplay(650, 300, 310, 260)
        self.action_trigger = None  # Variable para manejar la acción desde Tkinter

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            if self.action_trigger == "upload_file":
                print("bbbbbbbbbbbbbbbbbbb")
                self.upload_file()  # Llamar a la función cuando se activa la acción
                self.action_trigger = None  # Resetear la acción    

            self.screen.fill(GRAY)
            self.level.run()
            for button in self.buttons:
                button.draw(self.screen)
            self.tree_display.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

    def upload_file(self):
        print("aaaaaaaaaaaaaaaaaa")
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", initialdir=".",
                                                filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
        root.destroy()
        if file_path:
            mapa = ALFile(file_path)
            self.level.setMap(mapa)

# Función para ejecutar la ventana de Tkinter
def run_tkinter(game_instance):
    root = Tk()
    root.title("Interfaz de Usuario")

    # Aquí puedes agregar widgets y botones de Tkinter
    button = bt(root, text="Ejecutar acción en Pygame", command=lambda: execute_in_pygame(game_instance))
    button.pack()

    # Mantener la ventana abierta
    root.mainloop()

def execute_in_pygame(game_instance):
    game_instance.action_trigger = "upload_file"  # Establecer la acción a ejecutar

    
if __name__ == '__main__':
    game = Game()

    # Ejecutar Tkinter en un hilo separado y pasar la instancia del juego
    tkinter_thread = threading.Thread(target=run_tkinter, args=(game,))
    tkinter_thread.start()

    # Ejecutar el juego de Pygame
    game.run()