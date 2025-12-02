# --- TicTacToe klasse ---

class TicTacToe:
    def __init__(self, player=1, board=None):
        self.player_turn = player
        if board:
            self.board = board
        else:
            self.board = [[0,0,0],[0,0,0],[0,0,0]]

    def current_player(self):
        return self.player_turn

    def legal_move(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    moves.append(r*3 + c)
        return moves

    def make_move(self, move):
        row, col = move // 3, move % 3
        if self.board[row][col] != 0:
            raise ValueError("Invalid move: spot not empty")
        new_board = [row[:] for row in self.board]  # deepcopy
        new_board[row][col] = self.player_turn
        return TicTacToe(player = -self.player_turn, board=new_board)

    def is_terminal(self):
        lines = []
        lines.extend(self.board)  # rows
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])  # cols
        lines.append([self.board[i][i] for i in range(3)])  # diag1
        lines.append([self.board[i][2-i] for i in range(3)])  # diag2

        for line in lines:
            if abs(sum(line)) == 3:
                return True

        if all(cell != 0 for row in self.board for cell in row):
            return True

        return False

    def result(self):
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2-i] for i in range(3)])

        for line in lines:
            s = sum(line)
            if s == 3:
                return 1
            elif s == -3:
                return -1

        if all(cell != 0 for row in self.board for cell in row):
            return 0
        return None
