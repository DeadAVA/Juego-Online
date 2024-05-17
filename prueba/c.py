import socket
import pygame
import pickle

# Función para manejar la conexión con el servidor (Jugador 1 - Cubito Azul)
def handle_server(server_socket):
    try:
        # Configuración de Pygame para la ventana del cliente (cubito rojo para Jugador 2)
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        clock = pygame.time.Clock()

        # Posición inicial del cubito rojo en el cliente (Jugador 2)
        player2_pos = [300, 200]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Mover el cubito rojo (Jugador 2)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player2_pos[0] -= 5
                    elif event.key == pygame.K_d:
                        player2_pos[0] += 5
                    elif event.key == pygame.K_w:
                        player2_pos[1] -= 5
                    elif event.key == pygame.K_s:
                        player2_pos[1] += 5

            # Envía la posición del cubito rojo al servidor (Jugador 1)
            server_socket.sendall(pickle.dumps(player2_pos))

            # Recibe la posición del cubito azul del servidor (Jugador 1)
            data = server_socket.recv(1024)
            if data:
                player1_pos = pickle.loads(data)

                # Dibuja el cubito azul y el cubito rojo en la pantalla del cliente
                screen.fill((255, 0, 0))  # Color rojo
                pygame.draw.rect(screen, (255, 255, 255), (player1_pos[0], player1_pos[1], 50, 50))  # Cubito azul
                pygame.draw.rect(screen, (0, 0, 255), (player2_pos[0], player2_pos[1], 50, 50))  # Cubito rojo

            pygame.display.flip()
            clock.tick(60)  # Limitar la tasa de actualización de la pantalla

    finally:
        pygame.quit()
        server_socket.close()

# Configuración del cliente
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 5555))  # Conecta al servidor (Jugador 1)

# Inicia un hilo para manejar la conexión con el servidor (Jugador 1)
handle_server(server_socket)
