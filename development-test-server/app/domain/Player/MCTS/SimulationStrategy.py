from abc import ABC, abstractmethod

class SimulationStrategy(ABC):
    @abstractmethod
    def simulate(self, state, player):
        pass