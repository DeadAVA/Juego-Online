import socket

# Función para conectarse al servidor
def connect_to_server():
    host = '192.168.1.83'  # Dirección IP del servidor
    port = 12345  # Puerto para la conexión

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Conectado al servidor.")

    return client_socket

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

# Conectarse al servidor
server_conn = connect_to_server()

# Ejemplo de uso:
while True:
    move = input("Tu turno (por ejemplo, 'A1', 'B2', etc.): ")
    send_move(server_conn, move)

    move = receive_move(server_conn)
    print("El oponente hizo el movimiento:", move)

# Cerrar la conexión al final del juego
close_connection(server_conn)