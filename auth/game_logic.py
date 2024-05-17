class TicTacToe:
    def __init__(self):
        self.tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player1 = 1
        self.player2 = 2
        self.current_player = self.player1  # Comienza el jugador 1
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.tablero[row][col] == 0:
            self.tablero[row][col] = self.current_player
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_winner(self):
        # Implementa la lógica para verificar si hay un ganador
        # Devuelve el número del jugador ganador o 0 si no hay ganador
        winner = 0
        # Lógica para verificar filas, columnas y diagonales
        return winner
