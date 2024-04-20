import socket
import pygame as py
from constant import *
from game import *


HOST = '0.0.0.0'
PORT =  65432

def Game(tablero, event):
    if event.type == py.MOUSEBUTTONDOWN:
        x, y = py.mouse.get_pos()
        fila = y // TAMANO_CUADRO
        columna = x // TAMANO_CUADRO
        tablero.marcar(fila, columna)
    elif event.type == py.KEYDOWN:
        if event.key == py.K_RETURN and tablero.game_over:  
            tablero = Tablero()  
        elif event.key == py.K_ESCAPE and tablero.game_over:  
            return False  
    return True

def server():
    # Crear un socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the address and port
        s.bind((HOST, PORT))
        # Enable the server to accept connections
        s.listen()

        print(f"Servidor escuchando en {HOST}:{PORT}")
        
        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida desde {addr}")

            tablero = Tablero()
            game = True

            while game:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        game = False
                    else:
                        game = Game(tablero, event)

                # Envía el estado actual del juego al cliente
                game_state = tablero.get_game_state()
                conn.sendall(game_state.encode())

                # Recibe el movimiento del cliente y actualiza el estado del juego
                data = conn.recv(1024)
                if not data:
                    break
                # Procesa el movimiento del cliente y actualiza el estado del juego

                # Si el juego ha terminado, envía un mensaje al cliente y cierra la conexión
                

        print("Conexión cerrada")