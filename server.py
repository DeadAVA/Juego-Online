import socket
import pickle
from game import Tablero


HOST = '0.0.0.0'
PORT =  65432

class Servidor:
    def __init__(self, direccion, puerto):
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((direccion, puerto))
        self.servidor_socket.listen(1)
        self.cliente_socket, self.direccion_cliente = self.servidor_socket.accept()
        self.tablero = Tablero()
        self.game_loop()

    def game_loop(self):
        while True:
            # Lógica del juego
            self.cliente_socket.send(pickle.dumps(self.tablero))
            data = self.cliente_socket.recv(1024)
            fila, columna = pickle.loads(data)
            self.tablero.marcar(fila, columna)
            if self.tablero.game_over:
                self.cliente_socket.send(pickle.dumps(self.tablero))
                break

        self.cliente_socket.close()
        self.servidor_socket.close()

def server():
    servidor = Servidor(HOST, PORT)
