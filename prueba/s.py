import socket
import pygame
import pickle

# Función para manejar la conexión con el cliente (Jugador 2 - Cubito Rojo)
def handle_client(client_socket):
    try:
        print("Jugador 2 conectado.")

        # Configuración de Pygame para la ventana del servidor (cubito azul para Jugador 1)
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        clock = pygame.time.Clock()

        # Posición inicial del cubito azul en el servidor (Jugador 1)
        player1_pos = [50, 50]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Mover el cubito azul (Jugador 1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player1_pos[0] -= 5
                    elif event.key == pygame.K_RIGHT:
                        player1_pos[0] += 5
                    elif event.key == pygame.K_UP:
                        player1_pos[1] -= 5
                    elif event.key == pygame.K_DOWN:
                        player1_pos[1] += 5

            # Envía la posición del cubito azul al cliente (Jugador 2)
            client_socket.sendall(pickle.dumps(player1_pos))

            # Dibuja el cubito azul en la pantalla del servidor
            screen.fill((0, 0, 255))  # Color azul
            pygame.draw.rect(screen, (255, 255, 255), (player1_pos[0], player1_pos[1], 50, 50))

            pygame.display.flip()
            clock.tick(60)  # Limitar la tasa de actualización de la pantalla

    finally:
        pygame.quit()
        client_socket.close()

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
