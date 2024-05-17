import socket
import pygame
import pickle

# Configuración del tablero
BOARD_SIZE = 3
CELL_SIZE = 100
SCREEN_WIDTH = BOARD_SIZE * CELL_SIZE
SCREEN_HEIGHT = BOARD_SIZE * CELL_SIZE

# Función para manejar la conexión con el servidor (Jugador 1 - Cubito Azul)
def handle_server(server_socket):
    try:
        # Configuración de Pygame para la ventana del cliente (cubito rojo para Jugador 2)
        pygame.init()
        pygame.display.set_caption("jugador 2")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        running = True
        my_turn = False  # Variable para controlar el turno del jugador
        winner = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and my_turn and winner is None:
                    x, y = pygame.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE

                    # Enviar el movimiento al servidor (Jugador 1)
                    server_socket.sendall(pickle.dumps((row, col)))

                    # Esperar la respuesta del servidor (actualización del tablero)
                    data = server_socket.recv(1024)
                    if data:
                        try:
                            board = pickle.loads(data)
                            my_turn = False  # Cambiar turno después de hacer un movimiento
                        except pickle.UnpicklingError as e:
                            print("Error al deserializar los datos del servidor:", e)

            # Recibe y dibuja el estado actual del tablero del servidor (Jugador 1)
            data = server_socket.recv(1024)
            if data:
                try:
                    board = pickle.loads(data)

                    # Dibuja el tablero y las marcas en la pantalla del cliente
                    screen.fill((255, 255, 255))  # Fondo blanco
                    for row in range(BOARD_SIZE):
                        for col in range(BOARD_SIZE):
                            pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                            if board[row][col] != ' ':
                                font = pygame.font.Font(None, 100)
                                text_surface = font.render(board[row][col], True, (0, 0, 255) if board[row][col] == 'X' else (255, 0, 0))
                                screen.blit(text_surface, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))

                    pygame.display.flip()
                    clock.tick(60)  # Limitar la tasa de actualización de la pantalla

                except pickle.UnpicklingError as e:
                    print("Error al deserializar los datos del servidor:", e)

            # Verificar si hay un ganador
            winner = check_winner(board)
            if winner is not None:
                print(f"¡{winner} ha ganado!")
                running = False

            # Controlar el turno del jugador
            my_turn = (winner is None)  # Solo permite jugar si no hay ganador

    finally:
        pygame.quit()
        server_socket.close()

def check_winner(board):
    # Verificar filas
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Verificar columnas
    for col in range(BOARD_SIZE):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Verificar diagonales
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    # Si no hay ganador
    return None

# Configuración del cliente
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 5555))  # Conecta al servidor (Jugador 1)

# Inicia un hilo para manejar la conexión con el servidor (Jugador 1)
handle_server(server_socket)
