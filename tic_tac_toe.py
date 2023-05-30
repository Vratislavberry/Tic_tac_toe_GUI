import os
from copy import deepcopy

class Tic_tac_toe:
    def __init__(self):
        self.board_size = 15
        self.board = self._create_board()
        self.player_color = "blue"
        self.player_on_turn = "X"
        self.winner = ""
        self.win_symbols = []

    def _create_board(self):
        board = []
        for _ in range(self.board_size):
            row = ["" for _ in range(self.board_size)]
            board.append(row)
        return board


    def switch_player(self):
        self.player_on_turn = "X" if self.player_on_turn != "X" else "O"  # zmena hrace na konci kola
        self.player_color = "blue" if self.player_color != "blue" else "red"

    def make_turn(self, x, y):
        self.board[y][x] = self.player_on_turn

    def _horizontal_win(self):
        copied_board = deepcopy(self.board)
        for i, row in enumerate(copied_board): # Pro kazdy radek
            for _ in range(row.count(self.player_on_turn)): # Pro kazdy symbol aktualniho hrace na danem radku
                symbol_index = row.index(self.player_on_turn)
                #print(f"kontrolovanym symbolem bude {symbol_index} {i}")
                row[row.index(self.player_on_turn)] = "End" # pri pouziti funkce index je potreba zmenit "X" na neco jineho, aby to zachytavalo vsechna "X"
                if symbol_index >= 2 and symbol_index <= self.board_size-3: # Kontrola, abych nesel mimo pole
                    # Pokud jsou od symbolu hrace 2 stejne symboly na levo i na pravo
                    if row[symbol_index-2] in [self.player_on_turn, "End"] and row[symbol_index-1] in [self.player_on_turn, "End"]:
                        if row[symbol_index+1] in [self.player_on_turn, "End"] and row[symbol_index+2] in [self.player_on_turn, "End"]:
                            for a in range(-2, 3): # souradnice, ktere urci, ktere symboly budou vybarvene, kdyz nekdo vyhraje
                                self.win_symbols.append((symbol_index + a, i))
                            return 1

    def _vertical_win(self):
        copied_board = deepcopy(self.board)
        for i, row in enumerate(copied_board[2:13]):
            i += 2
            for _ in range(row.count(self.player_on_turn)):
                symbol_index = row.index(self.player_on_turn)
                row[row.index(self.player_on_turn)] = "End"
                if copied_board[i-2][symbol_index] in [self.player_on_turn, "End"] and copied_board[i-1][symbol_index] in [self.player_on_turn, "End"]:
                    if copied_board[i+1][symbol_index] in [self.player_on_turn, "End"] and copied_board[i+2][symbol_index] in [self.player_on_turn, "End"]:
                        for a in range(-2, 3): # souradnice, ktere urci, ktere symboly budou vybarvene, kdyz nekdo vyhraje
                            self.win_symbols.append((symbol_index, i+a))
                        return 1

    def _diagonal_win(self):
        copied_board = deepcopy(self.board)
        for i, row in enumerate(copied_board[2:13]):
            i += 2
            for _ in range(row.count(self.player_on_turn)):
                symbol_index = row.index(self.player_on_turn)
                row[row.index(self.player_on_turn)] = "End"
                if symbol_index >= 2 and symbol_index <= self.board_size - 3:
                    if copied_board[i-2][symbol_index-2] in [self.player_on_turn, "End"] and copied_board[i-1][symbol_index-1] in [self.player_on_turn, "End"]: # Natoceni piskvorek: \
                        if copied_board[i+1][symbol_index+1] in [self.player_on_turn, "End"] and copied_board[i+2][symbol_index+2] in [self.player_on_turn, "End"]:
                            for a in range(-2, 3):  # souradnice, ktere urci, ktere symboly budou vybarvene, kdyz nekdo vyhraje
                                self.win_symbols.append((symbol_index+a, i+a))
                            return 1
                    elif copied_board[i-2][symbol_index+2] in [self.player_on_turn, "End"] and copied_board[i-1][symbol_index+1] in [self.player_on_turn, "End"]: # Natoceni piskvorek: /
                        if copied_board[i+1][symbol_index-1] in [self.player_on_turn, "End"] and copied_board[i+2][symbol_index-2] in [self.player_on_turn, "End"]:
                            for a in range(-2, 3):  # souradnice, ktere urci, ktere symboly budou vybarvene, kdyz nekdo vyhraje
                                self.win_symbols.append((symbol_index-a, i+a))
                            return 1

    def _is_tie(self):
        for row in self.board:
            if row.count("") >= 1:
                return 0
        return 2



    def game_ended(self):
        if self._horizontal_win() or self._vertical_win() or self._diagonal_win():
            self.winner = self.player_on_turn
            return 1
        elif self._is_tie():
            return 2
        else:
            return 0

    def reset(self):
        self.__init__()



