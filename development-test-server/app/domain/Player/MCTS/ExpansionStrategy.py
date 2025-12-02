from abc import abstractmethod, ABC

class ExpansionStrategy(ABC):
    @abstractmethod
    def expand(self, node):
        pass