import random

from app.domain.Player.MCTS.RolloutStrategy import RolloutStrategy


class DefaultRolloutStrategy(RolloutStrategy):
    def select_move(self, state):
        current_player = state.current_player()
        for move in state.legal_move():
            if state.make_move(move).result() == current_player:
                return move
        opponent = -current_player
        for move in state.legal_move():
            if state.make_move(move).result() == opponent:
                return move
        return random.choice(state.legal_move())