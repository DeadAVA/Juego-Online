import socket

# Función para iniciar el servidor
def start_server():
    host = '192.168.1.83'  # Dirección IP local
    port = 12345  # Puerto para la conexión

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Acepta hasta 2 conexiones

    print("Esperando conexiones de jugadores...")
    player1_conn, player1_addr = server_socket.accept()
    print("Jugador 1 conectado:", player1_addr)
    player1_conn.send(b'You are Player 1')

    player2_conn, player2_addr = server_socket.accept()
    print("Jugador 2 conectado:", player2_addr)
    player2_conn.send(b'You are Player 2')

    return player1_conn, player2_conn

# Función para recibir jugadas
def receive_move(conn):
    move = conn.recv(1024).decode()
    print("Movimiento recibido:", move)
    return move

# Función para enviar jugadas
def send_move(conn, move):
    conn.send(move.encode())

# Función para cerrar la conexión
def close_connection(conn):
    conn.close()

# Iniciar el servidor
player1_conn, player2_conn = start_server()

# Ejemplo de uso:
while True:
    move = receive_move(player1_conn)
    print("Jugador 1 hizo el movimiento:", move)
    send_move(player2_conn, move)

    move = receive_move(player2_conn)
    print("Jugador 2 hizo el movimiento:", move)
    send_move(player1_conn, move)

# Cerrar conexiones al final del juego
close_connection(player1_conn)
close_connection(player2_conn)
