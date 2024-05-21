import pygame
import threading
import socket
import pickle
import select
from python_cliente import chat2

# Configuración del tablero
BOARD_SIZE = 3
CELL_SIZE = 100
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Inicializa el tablero con ' '
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
turn = None  # Inicia como None, esperando confirmación del servidor

# Colores
backgroundColor = (255, 255, 255)
titleColor = (0, 0, 0)
subtitleColor = (128, 0, 255)
lineColor = (0, 0, 0)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    
    for col in range(BOARD_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    
    if all(cell != ' ' for row in board for cell in row):
        return 'Empate'
    
    return None

def handle_input(server_socket):
    global turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':  # Solo permitir si es el turno de 'X'
            x, y = pygame.mouse.get_pos()
            col = (x - 100) // CELL_SIZE  # Ajustamos la coordenada x
            row = (y - 100) // CELL_SIZE  # Ajustamos la coordenada y

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:  # Verificamos que las coordenadas estén dentro del rango
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    turn = 'O'  # Cambia el turno al jugador 'O'
                    server_socket.sendall(pickle.dumps((board, turn)))  # Envía el tablero y el turno al servidor
                    return True

    return True

def draw_grid(screen):
    # Dibujar líneas verticales
    pygame.draw.line(screen, lineColor, (200, 100), (200, 400), 4)
    pygame.draw.line(screen, lineColor, (300, 100), (300, 400), 4)
    # Dibujar líneas horizontales
    pygame.draw.line(screen, lineColor, (100, 200), (400, 200), 4)
    pygame.draw.line(screen, lineColor, (100, 300), (400, 300), 4)

def draw_board(screen, message, bigfont, smallfont):
    screen.fill(backgroundColor)
    draw_grid(screen)  # Dibujar la cuadrícula
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell_content = board[row][col]
            if cell_content != ' ':
                font = pygame.font.Font(None, 100)
                if cell_content == 'X':
                    text_surface = font.render(cell_content, True, (0, 0, 255))  # Azul para 'X'
                else:
                   text_surface = font.render(cell_content, True, (255, 0, 0))  # Rojo para 'O'
                cell_x = col * CELL_SIZE + (CELL_SIZE - text_surface.get_width()) // 2 + 100  # Ajuste para centrar en la celda y desplazar a la derecha
                cell_y = row * CELL_SIZE + (CELL_SIZE - text_surface.get_height()) // 2 + 100  # Ajuste para centrar en la celda y desplazar hacia abajo
                screen.blit(text_surface, (cell_x, cell_y))

    title = bigfont.render("GATO", True, titleColor)
    screen.blit(title, (110, 0))
    subtitle = smallfont.render(str.upper(message), True, subtitleColor)
    screen.blit(subtitle, (150, 70))
    pygame.display.flip()

def center_message(screen, msg, smallfont, color = titleColor):
    pos = (100, 480)
    msg_rendered = smallfont.render(msg, True, color)
    screen.blit(msg_rendered, pos)

def cliente():
    global turn
    pygame.init()
    pygame.display.set_caption("Cliente")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Fuentes
    bigfont = pygame.font.Font('freesansbold.ttf', 64)
    smallfont = pygame.font.Font('freesansbold.ttf', 32)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.setblocking(0)
    
    chat_thread = threading.Thread(target=chat2)
    chat_thread.start()

    # Recibe el turno inicial del servidor
    while turn is None:
        ready_to_read, _, _ = select.select([client_socket], [], [], 0.1)
        if client_socket in ready_to_read:
            initial_data = client_socket.recv(4096)
            turn = pickle.loads(initial_data)

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

        winner = check_winner(board)
        if winner:
            if winner == 'Empate':
                center_message(screen, "EMPATE!", smallfont)
            else:
                center_message(screen, f"GANADOR: {winner}", smallfont)
            running = False
        else:
            draw_board(screen, f"Turno de {turn}", bigfont, smallfont)
            running = handle_input(client_socket)

        draw_board(screen, f"Turno de {turn}", bigfont, smallfont)

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    cliente()

