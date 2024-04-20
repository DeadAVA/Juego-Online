import socket
import pygame as py
from constant import *
from game import *

# Definir el host y puerto al que se conectará el cliente
HOST = '192.168.1.248'  # Dirección IP del servidor
PORT = 65432        # Puerto del servidor

def Game(tablero, event):
    if event.type == py.MOUSEBUTTONDOWN:
        # Lógica del juego para el cliente
        pass
    elif event.type == py.KEYDOWN:
        if event.key == py.K_RETURN and tablero.game_over:  
            tablero = Tablero()  
        elif event.key == py.K_ESCAPE and tablero.game_over:  
            return False  
    return True

def client():
    # Conectar al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Conexión establecida con el servidor")

        while True:
            # Recibe el estado actual del juego desde el servidor
            data = s.recv(1024)
            if not data:
                break
            game_state = data.decode()
            # Muestra el estado actual del juego al usuario

            # Si el juego ha terminado, muestra un mensaje y cierra la conexión
            if game_state == 'Game Over':
                print("El juego ha terminado.")
                break

            # Procesa el movimiento del jugador y envíalo al servidor

            # Si el juego ha terminado, envía un mensaje al servidor y cierra la conexión
            
