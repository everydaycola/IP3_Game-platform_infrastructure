import math
from copy import deepcopy
from typing import Optional

from app.domain.Player.MCTS import ExpansionStrategy, SimulationStrategy
from app.domain.Player.MCTS.DefaultExpansionStrategy import DefaultExpansionStrategy
from app.domain.Player.MCTS.DefaultSimulationStrategy import DefaultSimulationStrategy
from app.domain.Player.MCTS.DefaultRolloutStrategy import DefaultRolloutStrategy
from app.domain.Player.MCTS.MCTSNode import MCTSNode

class MCTS:
    def __init__(self, iterations=1000, exploration=math.sqrt(2),
                 expansion_strategy: ExpansionStrategy = None,
                 simulation_strategy: SimulationStrategy = None):
        self.iterations = iterations
        self.exploration = exploration
        # Use default strategies if none provided
        self.expansion_strategy = expansion_strategy or DefaultExpansionStrategy()
        self.simulation_strategy = simulation_strategy or DefaultSimulationStrategy(DefaultRolloutStrategy())

    def selection(self, root):
        node = root
        state = deepcopy(root.state)
        # Traverse tree towards the best child using UCT
        while node.untried_moves == [] and node.children:
            node = node.best_child(self.exploration)
            state = state.make_move(node.move)
        return node, state

    def expansion(self, node):
        # Use strategy pattern for expansion
        return self.expansion_strategy.expand(node)

    def simulation(self, state, player):
        # Use strategy pattern for simulation
        return self.simulation_strategy.simulate(state, player)

    def backpropagation(self, node, reward):
        # Update all ancestors with reward
        while node:
            node.visits += 1
            node.value += reward
            node = node.parent

    def search(self, initial_state: 'TicTacToe', root: Optional[MCTSNode] = None):
        if root is None or root.state != initial_state:
            root = MCTSNode(initial_state)
        root_player = initial_state.current_player()

        if not root.untried_moves and not root.children:
            # No moves possible, game over
            return -1, None

        for _ in range(self.iterations):
            node, state = self.selection(root)
            if node.untried_moves:
                node = self.expansion(node)
                if node:
                    state = node.state

            reward = self.simulation(state, root_player)
            self.backpropagation(node, reward)

        if not root.children:
            return -1, None

        best_child = max(root.children, key=lambda c: c.visits)
        move = best_child.move

        root.print_tree(max_depth=3)

        new_root = best_child
        new_root.parent = None

        return move, new_root
