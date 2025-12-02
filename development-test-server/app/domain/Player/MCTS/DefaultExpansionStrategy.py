import random

from app.domain.Player.MCTS.ExpansionStrategy import ExpansionStrategy
from app.domain.Player.MCTS.MCTSNode import MCTSNode


class DefaultExpansionStrategy(ExpansionStrategy):
    def expand(self, node):
        if not node.untried_moves:
            return None
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)
        new_state = node.state.make_move(move)
        child_node = MCTSNode(new_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node