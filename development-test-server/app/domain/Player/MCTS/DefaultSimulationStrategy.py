from copy import deepcopy

from app.domain.Player.MCTS.SimulationStrategy import SimulationStrategy


class DefaultSimulationStrategy(SimulationStrategy):
    def __init__(self, rollout_policy):
        self.rollout_policy = rollout_policy

    def simulate(self, state, player):
        sim_state = deepcopy(state)
        while not sim_state.is_terminal():
            move = self.rollout_policy.select_move(sim_state)
            sim_state = sim_state.make_move(move)
        sim_result = sim_state.result()
        if sim_result == player:
            return 1
        elif sim_result == 0:
            return 0
        else:
            return -1