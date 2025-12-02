from abc import abstractmethod, ABC

class RolloutStrategy(ABC):
    @abstractmethod
    def select_move(self, state):
        pass