import socket
import pygame as py
from pygame.locals import *
from constant import *

class Tablero:
    def __init__(self, bigfont, smallfont, player_id):
        self.tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_id = player_id
        self.opponent_id = 1 if player_id == 2 else 2
        self.game_over = False
        self.winner = None
        self.bigfont = bigfont
        self.smallfont = smallfont
        self.my_turn = player_id == 1
        
    def printCurrent(self, current, pos, screen, color):
        currentRendered = self.bigfont.render(str.upper(current), True, color)
        screen.blit(currentRendered, pos)
        
    def dibujar(self, screen, string, client_socket, playerColor=subtitleColor):
        screen.fill(WHITE)
        
        # Dibujar líneas del tablero
        py.draw.line(screen, lineColor, (250-2, 150), (250-2, 450), 4)
        py.draw.line(screen, lineColor, (350-2, 150), (350-2, 450), 4)
        py.draw.line(screen, lineColor, (150, 250-2), (450, 250-2), 4)
        py.draw.line(screen, lineColor, (150, 350-2), (450, 350-2), 4)
        
        # Renderizar título y subtítulo
        title = self.bigfont.render("TIC TAC TOE", True, titleColor)
        subtitle = self.smallfont.render(str.upper(string), True, playerColor)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        
        # Obtener datos del cliente
        client_data = self.get_client_data(client_socket)
        if client_data:
            data_decoded = client_data.decode().split(",")
            y_position = int(data_decoded[1])
            
            # Dibujar símbolos en el tablero según los datos recibidos
            for i in range(3):
                for j in range(3):
                    x = int((j + 1.8) * 100)
                    current = " "
                    color = titleColor
                    if self.tablero[i][j] == self.player_id:
                        current = "X" if self.player_id == 1 else "O"
                        color = playerOneColor if self.player_id == 1 else playerTwoColor
                    self.printCurrent(current, (x, y_position), screen, color)

    def get_client_data(self, client_socket):
        try:
            data = client_socket.recv(2048 * 10)
            client_socket.settimeout(20)
            return data
        except socket.timeout:
            return None
                
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
            col = int(x/100 - 1.5)
            row = int(y/100 - 1.5)
            print("({}, {})".format(row, col))
            if self.validate_input(row, col):
                if i % 2 == 0:
                    self.tablero[row][col] = self.player_id
                else: 
                    self.tablero[row][col] = self.opponent_id
                i += 1

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
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != 0:
                result = self.tablero[i][0]
                break
        return result

    def check_columns(self):
        result = 0
        for i in range(DIMENSION):
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != 0:
                result = self.tablero[0][i]
                break
        return result

    def check_diagonals(self):
        result = 0
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != 0:
            result = self.tablero[0][0]
        elif self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != 0:
            result = self.tablero[0][2]
        return result

    def check_winner(self):
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
        if result == self.player_id:
            msg = "¡Felicidades! ¡Eres el ganador!" if self.player_id == 1 else "¡El jugador dos es el ganador!"
            self.mensaje_centro(msg, screen, playerOneColor if self.player_id == 1 else playerTwoColor)
        elif result == self.opponent_id:
            msg = "¡Has perdido!" if self.player_id == 1 else "¡El jugador uno ha ganado!"
            self.mensaje_centro(msg, screen, playerTwoColor if self.player_id == 1 else playerOneColor)
        elif i >= 9:
            self.mensaje_centro("¡Empate! ¡Intente de nuevo más tarde!", screen)
        self.draw_bottom_texts(screen)


def server_connection(TCP_IP, TCP_PORT):
    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlazar el socket a la dirección y puerto
    server_socket.bind((TCP_IP, TCP_PORT))

    # Escuchar conexiones entrantes
    server_socket.listen(1)

    # Esperar a que un cliente se conecte
    print("Esperando conexiones...")
    client_socket, client_address = server_socket.accept()

    print("Conexión establecida con:", client_address)

    # Crear instancia de Tablero y dibujar pantalla inicial
    py.init()
    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    py.display.set_caption("Tic Tac Toe")
    bigfont = py.font.Font('freesansbold.ttf', 64)
    smallfont = py.font.Font('freesansbold.ttf', 32)
    tablero = Tablero(bigfont, smallfont, 1)  # Asignar player_id = 1 al primer cliente

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                break
            elif event.type == py.MOUSEBUTTONUP and tablero.my_turn:
                pos = py.mouse.get_pos()
                tablero.handle_mouse_event(pos)

        # Dibujar el tablero
        tablero.dibujar(screen, "En juego", client_socket)

        # Verificar ganador
        winner = tablero.check_winner()
        if winner != 0 or tablero.i >= 9:
            running = False

        # Actualizar pantalla
        py.display.update()

    # Cerrar la conexión con el cliente
    client_socket.close()
    server_socket.close()

# Configuración del servidor
TCP_IP = '0.0.0.0'  # Dirección IP donde se ejecuta el servidor
TCP_PORT = 5005

# Iniciar el servidor
server_connection(TCP_IP, TCP_PORT)
