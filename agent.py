"""
Code for Exercise 2. Fill in the marked TODOs in the methods and submit this file.
!DO NOT change other code or the method signatures!
"""
from abstract_agent import AbstractAgent
#TODO: You may add imports here. Apart from standard library packages, you may use pandas, scipy and numpy.

class Agent(AbstractAgent):

    def get_payment_basic(self, alpha: float, budget:float) -> float:
        """
        Exercise 1 a): Given the pay-off factor alpha and your agent's budget,
        return the payment that your agent contributes.
        :param alpha: Pay-off factor.
        :param budget: Budget that your agent is given.
        :return: The payment that your agent contributes.
        """

        # If alpha < 1, then contributing isn't worthwhile.
        if alpha < 1.0:
            return 0.0

        p = 0.5
        q = -0.5

        payout = (p * alpha + q) * budget

        return payout

    def get_payment_basic_subgroups(self, alpha: float, budget: float, subgroup_size: int,
                                    total_player_count: int) -> float:
        """
        Exercise 1 b): Given the pay-off factor alpha and your agent's budget,
        return the payment that your agent contributes. Your agent now competes in subgroups, we give you the size as an
        additional parameter.
        :param alpha: Pay-off factor.
        :param budget: Budget that your agent is given.
        :param subgroup_size: The number of players in the current subgroup (including your agent).
        :param total_player_count: The total numbers of players (including your agent).
        :return: The payment that your agent contributes
        """

        #TODO: Implement Exercise 1 b) here!
        return 0.0

    def get_payment_punishment(self, alpha: float, beta:float, budget:float, subgroup_size: int, total_player_count: int) -> float:
        """
        Exercise 2: Given the pay-off factor alpha, the punishment factor beta, and your agent's budget,
        return the payment that your agent contributes.
        :param alpha: Pay-off factor.
        :param beta: Punishment factor.
        :param budget: Budget that your agent is given.
        :param subgroup_size: The number of players in the current subgroup (including your agent).
        :param total_player_count: The total numbers of players (including your agent).
        :return: The payment that your agent contributes.
        """

        #TODO: Implement Exercise 2 here!
        return 0.0

    def get_payment_discrete(self, alpha: float, budget:float, cost:float, subgroup_size: int, total_player_count: int) -> float:
        """
        Exercise 3: Discrete Setting. Given the pay-off factor alpha, the cost of the project, the number of players,
        and your agent's budget, return the payment that your agent contributes.
        :param alpha: Pay-off factor.
        :param budget: Budget that your agent is given.
        :param cost: Cost for one unit of the discrete public project.
        :param subgroup_size: The number of players in the current subgroup (including your agent).
        :param total_player_count: The total numbers of players (including your agent).
        :return: The payment that your agent contributes.
        """

        #TODO: Implement Exercise 3 here!
        return 0.0