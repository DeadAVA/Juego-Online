import socket
import sys
import pygame as py
import pickle
from constant import *
from game import Tablero

# Definir el host y puerto al que se conectará el cliente
HOST = '192.168.1.241'  # Dirección IP del servidor
PORT = 65432        # Puerto del servidor

class Cliente:
    def __init__(self, direccion_servidor, puerto_servidor):
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((direccion_servidor, puerto_servidor))
        self.game_loop()

    def game_loop(self):
        while True:
            # Recibe el estado del tablero del servidor
            data = self.cliente_socket.recv(1024)
            tablero = pickle.loads(data)
            
            # Lógica del juego (entrada del jugador)
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN:
                    x, y = py.mouse.get_pos()
                    fila = y // TAMANO_CUADRO
                    columna = x // TAMANO_CUADRO
                    tablero.marcar(fila, columna)
            
            # Envía la acción del jugador al servidor
            self.cliente_socket.send(pickle.dumps((fila, columna)))
            
            # Verifica si el juego ha terminado
            if tablero.game_over:
                break

        self.cliente_socket.close()

def client():
    cliente = Cliente(HOST, PORT)
