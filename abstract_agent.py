from abc import ABC, abstractmethod

class AbstractAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    def get_payment_basic(self, alpha: float, budget: float) -> float:
        pass

    @abstractmethod
    def get_payment_basic_subgroups(self, alpha: float, budget: float, subgroup_size: int, total_player_count: int) -> float:
        pass

    @abstractmethod
    def get_payment_punishment(self, alpha: float, beta: float, budget: float, subgroup_size: int, total_player_count: int) -> float:
        pass

    @abstractmethod
    def get_payment_discrete(self, alpha: float, budget: float, cost: float, subgroup_size: int, total_player_count: int) -> float:
        pass
