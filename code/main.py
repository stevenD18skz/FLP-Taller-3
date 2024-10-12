import pygame
import sys
from settings import *
from level import Level
from tkinter import Tk, filedialog
from support import *

# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
BORDER_COLOR = (0, 0, 0)  # Color del borde


# Clase para crear botones
class Button:
    def __init__(self, text, x, y, width, height, font_size=36, color=LIGHT_GRAY, border_color=BORDER_COLOR, border_width=2):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.font = pygame.font.Font(None, font_size)  # Cambiar tamaño de la fuente
        self.active = True

    def draw(self, surface):
        # Color del botón
        button_color = self.color if self.active else DARK_GRAY
        pygame.draw.rect(surface, button_color, self.rect)

        # Dibuja el borde
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        # Dibuja el texto
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # Solo permite clics si el botón está activo
        if not self.active:
            return False
        return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        # Configuración general
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('POKEMON')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Configuración de botones
        self.algorithm_choice = 'No informada'
        self.buttons = [
            Button('No informada', 650, 40, 150, 40, font_size=24, color=LIGHT_GRAY),
            Button('Informada', 810, 40, 150, 40, font_size=24, color=LIGHT_GRAY),
            Button('Amplitud', 650, 110, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('Costo uniforme', 650, 170, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('Profundidad evitando ciclos', 650, 230, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('Avara', 810, 110, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('A*', 810, 170, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('REINICIAR', 650, 580, 100, 40, font_size=24, color=LIGHT_GRAY),
            Button('Subir archivo', 800, 580, 150, 40, font_size=24, color=LIGHT_GRAY)
        ]
        
        self.level.setMap(ALFile("C:/Users/braya/Desktop/FLP-Taller-3/entrada1.txt"))
        self.update_button_states()



    def update_button_states(self):
        if self.level.mapa == None:
            for button in self.buttons[:-1]:
                button.active = False
            return

        for button in self.buttons:
            button.active = True  # Reiniciar el estado de todos los botones


        if self.algorithm_choice == 'No informada':
            # Activar botones de algoritmos no informados y desactivar los de informados
            for button in self.buttons[2:5]:  # Amplitud, Costo uniforme, Profundidad evitando ciclos
                button.active = True

            for button in self.buttons[5:7]:  # Avara, A*
                button.active = False

        elif self.algorithm_choice == 'Informada':
            # Desactivar botones de algoritmos no informados y activar los de informados
            for button in self.buttons[2:5]:  # Amplitud, Costo uniforme, Profundidad evitando ciclos
                button.active = False

            for button in self.buttons[5:7]:  # Avara, A*
                button.active = True



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.is_clicked((x, y)):
                            if button.text in ['No informada', 'Informada']:
                                self.algorithm_choice = button.text
                                self.update_button_states()
                                button.border_color = (255, 112, 40)
                                

                            elif button.text == 'Subir archivo':
                                self.upload_file()
                                self.update_button_states()
                            
                            elif button.text == 'REINICIAR':
                                self.level.create_map()

                            else:
                                self.level.ejecutarAlgoritmo(button.text)
                                button.border_color = (0, 255, 0)
                                
            self.screen.fill(GRAY)
            self.level.run()
            
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


    def upload_file(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            initialdir=".",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        root.destroy()

        # Si seleccionó un archivo, procesarlo
        print(file_path)
        if file_path:
            mapa = ALFile(file_path)
            self.level.setMap(mapa)

        # Restablecer el foco a la ventana de Pygame
        pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()))

        # Opcional: también puedes usar pygame.event.clear() para limpiar eventos pendientes
        pygame.event.clear()





if __name__ == '__main__':
    game = Game()
    game.run()

