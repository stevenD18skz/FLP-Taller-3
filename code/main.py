import pygame
import sys
from settings import *
from level import Level
from tkinter import Tk, filedialog
from support import *
from tkinter import messagebox

# Definimos algunos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
BORDER_COLOR = (0, 0, 0)  # Color del borde
ORANGE = (255, 112, 40)  # Color naranja para selección de "Informada/No informada"
BLUE = (0, 0, 255)  # Color azul para selección de algoritmos


class InputBox:
    def __init__(self, x, y, w, h, font_size=24, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.color_inactive = BLACK
        self.color_active = ORANGE
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en el campo de entrada
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Cambiar el color del campo de entrada
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''  # Limpiar el campo de texto si se presiona Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Eliminar el último carácter
                else:
                    # Solo permitir números en el campo de entrada
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Dibujar el campo de texto
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def get_value(self):
        try:
            return int(self.text) if self.text != '' else 8  # Devolver 0 si está vacío
        except ValueError:
            return 0


# Clase para crear botones
class Button:
    def __init__(self, text, x, y, width, height, font_size=36, color=LIGHT_GRAY, border_color=BORDER_COLOR, border_width=2, selected=False):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.font = pygame.font.Font(None, font_size)
        self.active = True
        self.selected = selected # Estado de selección del botón

    def draw(self, surface):
        # Cambiar el color del botón según su estado de selección
        if not self.active:
            button_color = DARK_GRAY
        elif self.selected:
            button_color = BLUE if self.text in ['Amplitud', 'Costo uniforme', 'Profundidad evitando ciclos', 'Avara', 'A*'] else ORANGE
        else:
            button_color = self.color

        # Dibujar el botón
        pygame.draw.rect(surface, button_color, self.rect)

        # Dibujar el borde
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        # Dibujar el texto
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
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('POKEMON')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Variable para almacenar la solución del algoritmo
        self.solution = None  # Esto se actualizará cuando se ejecute un algoritmo
        self.mapa_eleccion = None
        self.font = pygame.font.SysFont(None, 18)

        # Condición para mostrar el recuadro con la información

        # Configuración de botones
        self.algorithm_choice = 'No informada'
        self.selected_algorithm_button = None  # Para almacenar el botón de algoritmo seleccionado

        self.buttons = [
            Button('No informada', 650, 40, 150, 40, font_size=24, color=LIGHT_GRAY, selected=False),
            Button('Informada', 810, 40, 150, 40, font_size=24, color=LIGHT_GRAY),
            Button('Amplitud', 650, 110, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('Costo uniforme', 650, 170, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('Profundidad evitando ciclos', 650, 230, 150, 40, font_size=15, color=LIGHT_GRAY),
            Button('Avara', 810, 110, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('A*', 810, 170, 150, 40, font_size=18, color=LIGHT_GRAY),
            Button('REINICIAR', 650, 580, 100, 40, font_size=24, color=LIGHT_GRAY),
            Button('Subir archivo', 800, 580, 150, 40, font_size=24, color=LIGHT_GRAY)
        ]

    
        self.input_box = InputBox(810, 230, 150, 40, font_size=24)

        self.update_button_states()


    def draw_text(self, surface, text, x, y, font):
        # Dibujar el texto en la pantalla
        text_surface = font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

    def update_button_states(self):
        # Si no hay mapa, desactivar todos los botones excepto el de subir archivo
        if self.level.mapa is None:
            for button in self.buttons[:-1]:
                button.active = False
            return

        # Activar todos los botones
        for button in self.buttons:
            button.active = True

        if self.solution: 
            for button in self.buttons[:-2]:
                button.active = False
            return


        # Actualizar botones según el algoritmo seleccionado
        if self.algorithm_choice == 'No informada':
            for button in self.buttons[2:5]:  # Amplitud, Costo uniforme, Profundidad evitando ciclos
                button.active = True
            for button in self.buttons[5:7]:  # Avara, A*
                button.active = False

        elif self.algorithm_choice == 'Informada':
            for button in self.buttons[2:5]:  # Amplitud, Costo uniforme, Profundidad evitando ciclos
                button.active = False
            for button in self.buttons[5:7]:  # Avara, A*
                button.active = True
        


        for button in self.buttons:
            button.selected = button.text in [self.selected_algorithm_button, self.algorithm_choice]



    def display_solution_info(self, surface):
        # Dibuja el recuadro de información
        info_rect = pygame.Rect(650, 300, 380, 250)  # Define el tamaño del recuadro
        pygame.draw.rect(surface, LIGHT_GRAY, info_rect)
        pygame.draw.rect(surface, BORDER_COLOR, info_rect, 2)  # Dibujar el borde del recuadro
        
        if self.solution:


            # Renderizar texto de solución
            font = pygame.font.Font(None, 24)
            info_lines = [
                f"Caminos encontrados con {self.selected_algorithm_button}:",
                f"Nodos expandidos: {self.solution['explored_nodes']}",
                f"Profundidad máxima del árbol: {self.solution['max_depth']}",
                f"Tiempo de cómputo: {self.solution['computation_time']} (S)",
                f"Costo: {self.solution.get('total_cost', "----")}",
                f"CAMINO: {self.solution['path']}"
            ]
            self.guardar_solucion(self.solution['tree'])

            # Dibujar cada línea de texto en el recuadro
            for i, line in enumerate(info_lines):
                text_surface = font.render(line, True, BLACK)
                surface.blit(text_surface, (660, 310 + i * 30))  # Posicionar cada línea de texto



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.is_clicked((x, y)):# and self.level.init_wait == -1 and self.level.init_final == -1:
                            if button.text in ['No informada', 'Informada']:
                                self.algorithm_choice = button.text

                            elif button.text in ['Amplitud', 'Costo uniforme', 'Profundidad evitando ciclos', 'Avara', 'A*']:
                                self.selected_algorithm_button = button.text
                                valor = self.input_box.get_value()  # Obtener el valor numérico del input
                                self.level.ejecutarAlgoritmo(button.text, valor)
                                self.solution = self.level.solucion

                            elif button.text == 'Subir archivo':
                                self.solution = None
                                self.algorithm_choice = 'No informada'
                                self.selected_algorithm_button = None

                                self.level = Level()
                                self.upload_file()

                            elif button.text == 'REINICIAR':
                                self.solution = None
                                self.algorithm_choice = 'No informada'
                                self.selected_algorithm_button = None

                                self.level = Level()
                                self.level.setMap(self.mapa_eleccion)

                            self.update_button_states()


                # Manejar eventos del campo de texto
                self.input_box.handle_event(event)


            # Dibujar los botones y actualizar la pantalla
            self.screen.fill(GRAY)
            self.level.run()
            
            for button in self.buttons:
                button.draw(self.screen)


            # Dibujar el campo de entrada
            self.input_box.draw(self.screen)

            # Mostrar información de la solución si existe
            self.display_solution_info(self.screen)
            self.draw_text(self.screen, "Velocidad de animación del árbol (s/100), 0 para no ver animacion", 810, 278, self.font)
            self.draw_text(self.screen, "0 para no ver animacion", 810, 288, self.font)


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

        if not file_path:
            # Mostrar advertencia si no se selecciona un archivo
            messagebox.showwarning("Advertencia", "No seleccionaste un archivo de mapa.")
            return

        try:
            analizar_mapa = ALFile(file_path)
        except:
            # Mostrar error si hay un problema al analizar el archivo
            messagebox.showerror("Error", "Archivo de mapa inválido. Por favor, selecciona un archivo válido.")
            return

        self.mapa_eleccion = analizar_mapa
        self.level.setMap(analizar_mapa)

        pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()))
        pygame.event.clear()


    def guardar_solucion(self, solucion_outPut):
        with open('./arbol_busqueda.txt', 'w') as file:
            file.write(solucion_outPut)



if __name__ == '__main__':
    game = Game()
    game.run()

