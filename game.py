import pygame as py
import sys
from constant import *


class Tablero:
    def __init__(self, bigfont, smallfont):
        self.tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player1 = 1
        self.player2 = 2
        self.game_over = False
        self.winner = None  # Variable para almacenar al ganador
        self.bigfont = bigfont
        self.smallfont = smallfont
        
        
    def printCurrent(self, current, pos, screen, color):
        currentRendered = self.bigfont.render(str.upper(current), True, color)
        screen.blit(currentRendered, pos)
        
    def dibujar(self, screen, string, playerColor=subtitleColor):
        screen.fill(WHITE)
        
        # Líneas verticales
        py.draw.line(screen, lineColor, (250-2, 150), (250-2, 450), 4)
        py.draw.line(screen, lineColor, (350-2, 150), (350-2, 450), 4)
        # Líneas horizontales
        py.draw.line(screen, lineColor, (150, 250-2), (450, 250-2), 4)
        py.draw.line(screen, lineColor, (150, 350-2), (450, 350-2), 4)
        
        title = self.bigfont.render("TIC TAC TOE", True, titleColor)
        subtitle = self.smallfont.render(str.upper(string), True, playerColor)

        # Calcular las posiciones para centrar el texto
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        for i in range(3):
            for j in range(3):
                # Calcular las posiciones para centrar el texto en cada celda
                x = int((j + 1.8) * 100)
                y = int((i + 1.6) * 100)
                current = " "
                color = titleColor
                if self.tablero[i][j] == self.player1:
                    current = "X"
                    color = playerOneColor
                elif self.tablero[i][j] == self.player2:
                    current = "O"
                    color = playerTwoColor
                self.printCurrent(current, (x, y), screen, color)
                
    def mensaje_centro(self, msg, screen, color=titleColor):
        pos = (100, 400)
        msg_rendered = self.smallfont.render(msg, True, color)
        screen.blit(msg_rendered, pos)
        
    def draw_bottom_texts(self, screen):
        texto_reiniciar = self.smallfont.render("Enter para Reiniciar Partida", True, BLACK)
        texto_regresar = self.smallfont.render("ESC para Regresar al Menú", True, BLACK)
        screen.blit(texto_reiniciar, (10, SCREEN_HEIGHT - 40))
        screen.blit(texto_regresar, (10, SCREEN_HEIGHT - 20))
        
    def handle_mouse_event(self, pos):
        global i
        x = pos[0]
        y = pos[1]
        if(x < 150 or x > 450 or y < 150 or y > 450 or self.game_over or i >= 9):
            return
        else:
            # Cuando x aumenta, cambia la columna
            col = int(x/100 - 1.5)
            # Cuando y aumenta, cambia la fila
            row = int(y/100 - 1.5)
            print("({}, {})".format(row,col))
            if self.validate_input(row, col):
                if i % 2 == 0:
                    self.tablero[row][col] = self.player1
                else: 
                    self.tablero[row][col] = self.player2
                i = i + 1

    def validate_input(self, x, y):
        if x >= DIMENSION or y >= DIMENSION:
            print("\nFuera de límites! Intente de nuevo...\n")
            return False
        elif self.tablero[x][y] != 0:
            print("\nYa ingresado! Intente de nuevo...\n")
            return False
        return True

    def check_rows(self):
        result = 0
        for i in range(DIMENSION):
            if self.tablero[i][0] == self.tablero[i][1] and self.tablero[i][1] == self.tablero[i][2]:
                result = self.tablero[i][0]
                if result != 0:
                    break
        return result

    def check_columns(self):
        result = 0
        for i in range(DIMENSION):
            if self.tablero[0][i] == self.tablero[1][i] and self.tablero[1][i] == self.tablero[2][i]:
                result = self.tablero[0][i]
                if result != 0:
                    break
        return result

    def check_diagonals(self):
        result = 0
        if self.tablero[0][0] == self.tablero[1][1] and self.tablero[1][1] == self.tablero[2][2]:
            result = self.tablero[0][0]
        elif self.tablero[0][2] == self.tablero[1][1] and self.tablero[1][1] == self.tablero[2][0]:
            result = self.tablero[0][2]
        return result

    def check_winner(self):
        result = 0
        result = self.check_rows()
        if result == 0:
            result = self.check_columns()
        if result == 0:
            result = self.check_diagonals()
            
        if result != 0 or i >= 9:
            self.game_over = True
        return result

    def build_final_screen(self, screen, result):
        self.dibujar(screen, "~~~Game Over~~~")
        if result == self.player1:
            self.mensaje_centro("¡El jugador uno es el ganador!", screen, playerOneColor)
        elif result == self.player2:
            self.mensaje_centro("¡El jugador dos es el ganador!", screen, playerTwoColor)
        elif i >= 9:
            self.mensaje_centro("¡Empate! ¡Intente de nuevo más tarde!", screen)
        self.draw_bottom_texts(screen)


def start_game():
    py.init()
    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    py.display.set_caption("Tic Tac Toe")
    # Inicializar fuentes después de inicializar Pygame
    bigfont = py.font.Font('freesansbold.ttf', 64)
    smallfont = py.font.Font('freesansbold.ttf', 32)

    # Loop principal del juego
    tablero = Tablero(bigfont, smallfont)
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONUP:
                pos = py.mouse.get_pos()
                tablero.handle_mouse_event(pos)
            elif event.type == py.KEYDOWN:
                if event.key == py.K_RETURN and tablero.game_over:
                    tablero = Tablero(bigfont, smallfont)  # Reiniciar el juego
                elif event.key == py.K_ESCAPE and tablero.game_over:
                    running = False  # Salir del bucle y regresar al menú
        
        if i % 2 == 0:
            tablero.dibujar(screen, "Turno del jugador uno", playerOneColor)
        else:
            tablero.dibujar(screen, "Turno del jugador dos", playerTwoColor)

        result = tablero.check_winner()
        if i >= 9 or result != 0:
            tablero.build_final_screen(screen, result)

        # Actualizar pantalla
        py.display.update()

    py.quit()
i = 0


