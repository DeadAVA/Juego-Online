import pygame
import socket
import pickle
import select

# Configuración del tablero
BOARD_SIZE = 3
CELL_SIZE = 100
SCREEN_WIDTH = BOARD_SIZE * CELL_SIZE
SCREEN_HEIGHT = BOARD_SIZE * CELL_SIZE

# Inicializa el tablero con ' '
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def handle_input(server_socket):
    # Verifica el clic del mouse y actualiza el tablero
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if board[row][col] == ' ':
                board[row][col] = 'X'
                server_socket.sendall(pickle.dumps(board))  # Envía el tablero al servidor
                return True

    return True

def draw_board(screen):
    # Dibuja el tablero en la pantalla
    screen.fill((255, 255, 255))  # Fondo blanco
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[row][col] != ' ':
                font = pygame.font.Font(None, 100)
                text_surface = font.render(board[row][col], True, (0, 0, 255))
                screen.blit(text_surface, (col * CELL_SIZE + 20, row * CELL_SIZE + 20))

    pygame.display.flip()

def main():
    # Configuración de Pygame para la ventana del cliente
    pygame.init()
    pygame.display.set_caption("Cliente")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Configuración del socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))  # Conecta al servidor
    client_socket.setblocking(0)  # Configura el socket como no bloqueante

    running = True
    while running:
        pygame.event.pump()  # Procesa eventos de Pygame

        ready_to_read, _, _ = select.select([client_socket], [], [], 0.1)  # Verifica si hay datos para leer en el socket
        if client_socket in ready_to_read:
            data = client_socket.recv(4096)
            if data:
                new_board = pickle.loads(data)
                if new_board != board:
                    board[:] = new_board

        running = handle_input(client_socket)
        draw_board(screen)

    pygame.quit()

    # Cierra el socket del cliente
    client_socket.close()

if __name__ == "__main__":
    main()
