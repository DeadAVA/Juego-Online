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
turn = 'X'  # Inicia con 'O' para que el servidor comience

def handle_input(server_socket):
    global turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':  # Solo permitir si es el turno de 'X'
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if board[row][col] == ' ':
                board[row][col] = 'X'
                turn = 'O'  # Cambia el turno al jugador 'O'
                server_socket.sendall(pickle.dumps((board, turn)))  # Envía el tablero y el turno al servidor
                return True

    return True

def draw_board(screen):
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
    global turn
    pygame.init()
    pygame.display.set_caption("Cliente")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.setblocking(0)

    running = True
    while running:
        pygame.event.pump()

        ready_to_read, _, _ = select.select([client_socket], [], [], 0.1)
        if client_socket in ready_to_read:
            data = client_socket.recv(4096)
            if data:
                new_board, new_turn = pickle.loads(data)
                if new_board != board:
                    board[:] = new_board
                    turn = new_turn

        running = handle_input(client_socket)
        draw_board(screen)

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    main()
