import pygame as py
import sys
from constant import *



#Creamos la clase del tablero
class Tablero:
    def __init__(self):
        self.tablero = [['' for _ in range(DIMENSION)] for _ in range(DIMENSION)]
        self.turno = 1  # Jugador 1 inicia
        self.game_over = False

    def dibujar(self, screen):
        screen.fill(WHITE)
        for fila in range(DIMENSION):
            for columna in range(DIMENSION):
                py.draw.rect(screen, BLACK, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO), 3)
                texto = py.font.Font(None, 60).render(self.tablero[fila][columna], True, BLACK)
                screen.blit(texto, (columna * TAMANO_CUADRO + 20, fila * TAMANO_CUADRO + 20))
        if self.game_over and self.winner:  # Si hay un ganador y el ganador está definido
            texto_ganador = py.font.Font(None, 60).render(f'Ganador: {self.winner}', True, RED)
            screen.blit(texto_ganador, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - (-20)))
            
            reiniciar_rect = py.Rect(150, 400, 300, 50)
            py.draw.rect(screen, GREEN, reiniciar_rect)
            texto_reiniciar = py.font.Font(None, 40).render("Enter para Reiniciar Partida", True, BLACK)
            screen.blit(texto_reiniciar, (reiniciar_rect.centerx - texto_reiniciar.get_width() // 2, reiniciar_rect.centery - texto_reiniciar.get_height() // 2))

            # Dibujar botón de regresar al menú
            regresar_rect = py.Rect(150, 470, 300, 50)
            py.draw.rect(screen, GREEN, regresar_rect)
            texto_regresar = py.font.Font(None, 40).render("ESC para Regresar al Menú", True, BLACK)
            screen.blit(texto_regresar, (regresar_rect.centerx - texto_regresar.get_width() // 2, regresar_rect.centery - texto_regresar.get_height() // 2))
                
    def marcar(self, fila, columna):
        if not self.game_over and self.tablero[fila][columna] == '':
            if self.turno == 1:
                self.tablero[fila][columna] = 'X'
                self.turno = 2
            else:
                self.tablero[fila][columna] = 'O'
                self.turno = 1
            self.verificar_ganador()

    def verificar_ganador(self):
        for fila in range(DIMENSION):
            if self.tablero[fila][0] == self.tablero[fila][1] == self.tablero[fila][2] != '':
                self.game_over = True
                self.winner = self.tablero[fila][0]
                return
        for columna in range(DIMENSION):
            if self.tablero[0][columna] == self.tablero[1][columna] == self.tablero[2][columna] != '':
                self.game_over = True
                self.winner = self.tablero[0][columna]
                return
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != '':
            self.game_over = True
            self.winner = self.tablero[0][0]
            return
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != '':
            self.game_over = True
            self.winner = self.tablero[0][2]
            return
        if all(self.tablero[fila][columna] != '' for fila in range(DIMENSION) for columna in range(DIMENSION)):
            self.game_over = True
            
        

def Game_solo():
    # Estructura del juego
    py.init()

    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    py.display.set_caption("El gato")
    clock = py.time.Clock()

    tablero = Tablero()
    game = True

    while game:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                x, y = py.mouse.get_pos()
                fila = y // TAMANO_CUADRO
                columna = x // TAMANO_CUADRO
                tablero.marcar(fila, columna)
            elif event.type == py.KEYDOWN:
                if event.key == py.K_RETURN and tablero.game_over:  # Si se presiona Enter y el juego ha terminado
                    tablero = Tablero()  # Reiniciar el juego
                elif event.key == py.K_ESCAPE and tablero.game_over:  # Si se presiona ESC y el juego ha terminado
                    game = False  # Salir del bucle y regresar al menú

        tablero.dibujar(screen)
        py.display.flip()
        clock.tick(60)

    return

