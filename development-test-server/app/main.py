from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.domain.Player.MCTS.MCTS import MCTS
from app.domain.GameState.TicTacToe import TicTacToe

# --- FastAPI setup ---
app = FastAPI()
mcts = MCTS(iterations=50000)  # configureer aantal iteraties

class MoveRequest(BaseModel):
    boardState: List[List[str]]
    currentPlayer: str

class MoveResponse(BaseModel):
    best_move: int
    row: int
    col: int

def convert_board_state(board_state):
    if len(board_state) != 3:
        raise HTTPException(status_code=400, detail="Board must be 3x3")

    converted_board = []
    for row in board_state:
        if len(row) != 3:
            raise HTTPException(status_code=400, detail="Board must be 3x3")
        try:
            converted_board.append([int(cell) for cell in row])
        except ValueError:
            raise HTTPException(status_code=400, detail="Board must contain valid integers strings")
    return converted_board

def index_to_row_col(index):
    if not isinstance(index, int):
        raise TypeError("Invalid move index")
    if index < 0 or index >= 9:
        raise ValueError(f"Invalid move index: {index}")
    return index // 3, index % 3

@app.post("/ai-move", response_model=MoveResponse)
def get_best_move(request: MoveRequest):
    board_int = convert_board_state(request.boardState)
    try:
        current_player = int(request.currentPlayer)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid currentPlayer: expected '1' or '-1'.")

    if current_player not in [1, -1]:
        raise HTTPException(status_code=400, detail="Invalid currentPlayer: expected '1' or '-1'.")

    state = TicTacToe(player=current_player, board=board_int)

    if state.is_terminal():
        # Spel voorbij, geen zetten meer
        return MoveResponse(best_move=-1, row=-1, col=-1)

    best_move, _ = mcts.search(state, root=None)

    if best_move == -1:
        return MoveResponse(best_move=-1, row=-1, col=-1)

    row, col = index_to_row_col(best_move)
    return MoveResponse(best_move=best_move, row=row, col=col)
