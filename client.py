import pygame as py
import sys
import pickle
import socket
from constant import *


# Definir el host y puerto al que se conectará el cliente
HOST = '192.168.1.241'  # Dirección IP del servidor
PORT = 65432        # Puerto del servidor


class Cliente:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.host, self.puerto))
        self.tablero = None

    def recibir_estado(self):
        data = self.cliente_socket.recv(1024)
        self.tablero = pickle.loads(data)

    def enviar_movimiento(self, fila, columna):
        data = pickle.dumps((fila, columna))
        self.cliente_socket.send(data)

    def cerrar_conexion(self):
        self.cliente_socket.close()

def Game_online():
    # Estructura del juego
    py.init()

    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    py.display.set_caption("El gato")
    clock = py.time.Clock()

    cliente = Cliente('localhost', 65432)
    game = True

    while game:
        for event in py.event.get():
            if event.type == py.QUIT:
                cliente.cerrar_conexion()
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                x, y = py.mouse.get_pos()
                fila = y // TAMANO_CUADRO
                columna = x // TAMANO_CUADRO
                cliente.enviar_movimiento(fila, columna)

        cliente.recibir_estado()
        cliente.tablero.dibujar(screen)
        py.display.flip()
        clock.tick(60)

    return
