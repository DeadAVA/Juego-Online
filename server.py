import socket
import pickle
from game import Tablero

HOST = '0.0.0.0'
PORT =  65432

class Servidor:
    def __init__(self, direccion, puerto):
        self.host = direccion
        self.port = puerto
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.tablero = Tablero()

    def iniciar_servidor(self):
        self.servidor_socket.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}")

        cliente_socket, _ = self.servidor_socket.accept()
        print("Conexión aceptada.")

        try:
            while True:
                # Envía el estado del tablero al cliente
                cliente_socket.send(pickle.dumps(self.tablero))

                # Recibe la acción del cliente
                data = cliente_socket.recv(1024)
                if not data:
                    break
                
                fila, columna = pickle.loads(data)
                
                # Marca la casilla en el tablero
                self.tablero.marcar(fila, columna)
                
                # Verifica si el juego ha terminado
                if self.tablero.game_over:
                    # Envía el estado final del juego al cliente
                    cliente_socket.send(pickle.dumps(self.tablero))
                    break
        except Exception as e:
            print(f"Error al manejar cliente: {e}")
        finally:
            cliente_socket.close()
            self.servidor_socket.close()
def server():
    # Uso del servidor
    servidor = Servidor(HOST, PORT)
    servidor.iniciar_servidor()
