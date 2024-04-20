
import pygame as py
import sys
from constants import *
from game import Game


# Clase del botón
class Button:
    def __init__(self, x, y, width, height, text, text_color, color):
        self.rect = py.Rect(x, y, width, height)
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.color = color

    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

# Inicializar Pygame
py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Menú de Juego")
font = py.font.Font(None, 36)

# Función para mostrar el menú principal
def main_menu():
    play_button = Button(300, 200, 200, 50, "Jugar", BLACK, GREEN)
    multi_button = Button(300, 300, 200, 50, "Localhost", BLACK, GREEN)
    quit_button = Button(300, 400, 200, 50, "Salir", BLACK, GREEN)

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    # Lógica para iniciar el juego
                    print("selecciona jugador")
                elif multi_button.rect.collidepoint(event.pos):
                    print("se entro al multi")
                elif quit_button.rect.collidepoint(event.pos):
                    py.quit()
                    sys.exit()

        screen.fill(WHITE)
        play_button.draw(screen)
        multi_button.draw(screen)
        quit_button.draw(screen)
        py.display.flip()

# Ejecutar el menú principal
main_menu()
 