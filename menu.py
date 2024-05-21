import pygame as py
import sys
from constant import * 
from multiplayer_menu import MultiplayerMenu
from game import start_game

# Enumeración para los estados del menú
class MenuState:
    MAIN_MENU = 0
    MULTIPLAYER_MENU = 1

current_menu = MenuState.MAIN_MENU  # Inicializar el menú actual como el menú principal

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
icon = py.image.load("tictactoe.png")
py.display.set_icon(icon)
font = py.font.Font(None, 36)

# Función para mostrar el menú principal
def menu():
    play_button = Button(200, 200, 200, 50, "Jugar", BLACK, GREEN)
    multi_button = Button(200, 300, 200, 50, "MultiPlayer", BLACK, GREEN)
    quit_button = Button(200, 400, 200, 50, "Salir", BLACK, GREEN)

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    start_game()  # Cambiar al menú de juego
                elif multi_button.rect.collidepoint(event.pos):
                    MultiplayerMenu()  # Cambiar al menú de multiplayer
                elif quit_button.rect.collidepoint(event.pos):
                    py.quit()
                    sys.exit()

        screen.fill(WHITE)
        play_button.draw(screen)
        multi_button.draw(screen)
        quit_button.draw(screen)
        py.display.flip()

# Ejecutar el menú principal 
menu()
