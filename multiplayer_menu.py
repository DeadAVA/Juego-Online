import pygame as py
import sys
from auth.constant import * 

# Clase del botón
class Button:
    def __init__(self, x, y, width, height, text, text_color, color):
        self.rect = py.Rect(x, y, width, height)
        self.font = py.font.Font(None, 36)
        self.text_surf = self.font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.color = color

    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

# Función para mostrar el menú de multiplayer
def MultiplayerMenu():
    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = py.image.load("tictactoe.png")
    py.display.set_icon(icon)
    create_button = Button(200, 200, 200, 50, "Crear Server", BLACK, GREEN)
    join_button = Button(200, 300, 200, 50, "Unirse", BLACK, GREEN)
    back_button = Button(200, 400, 200, 50, "Regresar", BLACK, GREEN)

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                if create_button.rect.collidepoint(event.pos):
                    print("server")
                elif join_button.rect.collidepoint(event.pos):
                    print("Game_online()")
                elif back_button.rect.collidepoint(event.pos):
                    return  # Regresar al menú principal

        screen.fill(WHITE)
        create_button.draw(screen)
        join_button.draw(screen)
        back_button.draw(screen)
        py.display.flip()

