import socket
import pygame
import pickle

# Configuración del tablero
BOARD_SIZE = 3
CELL_SIZE = 100
SCREEN_WIDTH = BOARD_SIZE * CELL_SIZE
SCREEN_HEIGHT = BOARD_SIZE * CELL_SIZE

# Función para manejar la conexión con el cliente (Jugador 2 - Cubito Rojo)
def handle_client(client_socket):
    try:
        print("Jugador 2 conectado.")

        # Configuración de Pygame para la ventana del servidor (cubito azul para Jugador 1)
        pygame.init()
        pygame.display.set_caption("jugador 1")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        # Inicializar el tablero como vacío
        board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        running = True
        turn = 'X'  # 'X' comienza primero
        winner = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                    x, y = pygame.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE

                    # Verificar si la casilla está vacía y es el turno del jugador
                    if board[row][col] == ' ' and turn == 'X':
                        board[row][col] = 'X'
                        turn = 'O'  # Cambiar turno

            # Envía el estado actual del tablero al cliente (Jugador 2)
            client_socket.sendall(pickle.dumps(board))

            # Dibuja el tablero y las marcas en la pantalla del servidor
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

            # Verificar ganador
            winner = check_winner(board)

            if winner is not None:
                print(f"¡{winner} ha ganado!")
                running = False

    finally:
        pygame.quit()
        client_socket.close()

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

# Configuración del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5555))  # Asigna una dirección y puerto
server_socket.listen(1)  # Espera una conexión (Jugador 2)

print("Esperando la conexión del Jugador 2...")

# Espera la conexión del cliente (Jugador 2)
client_socket, address = server_socket.accept()
print("Jugador 2 conectado desde:", address)

# Inicia un hilo para manejar la conexión con el cliente (Jugador 2)
handle_client(client_socket)

# Cierra el socket del servidor
server_socket.close()
