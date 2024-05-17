import socket
import pygame as py
from pygame.locals import *
from constant import *  # Asegúrate de importar tus constantes como SCREEN_WIDTH, SCREEN_HEIGHT, etc.

class TicTacToeClient:
    def __init__(self, player_id):
        self.player_id = player_id
        self.server_address = '192.168.1.83'  # Dirección IP del servidor
        self.server_port = 5005  # Puerto en el que el servidor está escuchando
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Intentar conectarse al servidor
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print("Conexión establecida con el servidor.")
            self.connected = True
        except Exception as e:
            print("Error al conectar con el servidor:", e)
            self.connected = False

    def run_game(self):
        if not self.connected:
            return
        
        py.init()
        screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        py.display.set_caption("Tic Tac Toe")
        bigfont = py.font.Font('freesansbold.ttf', 64)
        smallfont = py.font.Font('freesansbold.ttf', 32)
        
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == py.MOUSEBUTTONUP:
                    if event.button == 1:  # Solo manejar clic izquierdo del mouse
                        pos = py.mouse.get_pos()
                        row = pos[1] // 100
                        col = pos[0] // 100
                        move = f"{row},{col}"
                        self.client_socket.send(move.encode())

            # Recibir y procesar actualizaciones del servidor
            try:
                data = self.client_socket.recv(1024)
                if data:
                    # Decodificar datos recibidos del servidor
                    decoded_data = data.decode()
                    if decoded_data == "GAME_OVER":
                        running = False
                    else:
                        # Actualizar el estado del juego en la pantalla
                        self.draw_board(screen, decoded_data, bigfont, smallfont)
                        py.display.update()
            except socket.error as e:
                print("Error de conexión con el servidor:", e)
                running = False

        # Cerrar la conexión al finalizar el juego
        self.client_socket.close()

    def draw_board(self, screen, board_state, bigfont, smallfont):
        screen.fill(WHITE)

        # Dibujar líneas del tablero
        py.draw.line(screen, lineColor, (250-2, 150), (250-2, 450), 4)
        py.draw.line(screen, lineColor, (350-2, 150), (350-2, 450), 4)
        py.draw.line(screen, lineColor, (150, 250-2), (450, 250-2), 4)
        py.draw.line(screen, lineColor, (150, 350-2), (450, 350-2), 4)

        # Renderizar título
        title = bigfont.render("TIC TAC TOE", True, titleColor)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)

        # Dibujar símbolos en el tablero basado en el estado recibido
        board_data = board_state.split(',')
        for i in range(3):
            for j in range(3):
                x = 100 * j + 160
                y = 100 * i + 160
                index = i * 3 + j
                if board_data[index] == '1':
                    symbol = "X"
                    color = playerOneColor
                elif board_data[index] == '2':
                    symbol = "O"
                    color = playerTwoColor
                else:
                    symbol = " "
                    color = titleColor
                symbol_rendered = bigfont.render(symbol, True, color)
                screen.blit(symbol_rendered, (x, y))

    def start(self):
        self.run_game()

if __name__ == "__main__":
    client = TicTacToeClient(player_id=2)
    client.start()