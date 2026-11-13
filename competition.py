"""
Simulation of the competition. You do not need to submit this file and may change it. Note that we may use different
values for the parameters in the final competition.
"""
import importlib.util
import itertools
import os
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import pyplot as plt

import dummy_agent
import agent
import logging
from abstract_agent import AbstractAgent

def get_agents():
    return [
        agent.Agent("Your agent"),
        *[
            dummy_agent.Agent(f"Dummy {i}")
            for i in range(1, 5)
        ],
    ]

class Competition:
    def __init__(self, subgroup_ratio: float):
        """
        Initializes the competition. Every round for Ex 1 b) - 3 will be played in all possible subgroups
        of size max(2, floor(number_agents/subgroup_ratio)). The final payoff is given by the sum of the payoffs that each agent
        achieves in every round the participate in.
        :param subgroup_ratio: Defines how small or large the subsets that the agents compete against are.
        Each subgroup has size max(2, floor(number_agents/subgroup_ratio)).
        """
        if subgroup_ratio < 1.0:
            raise ValueError("Subgroup ratio must be greater than or equal to 1.0.")
        self.agents: list[AbstractAgent] = get_agents()
        self.subgroup_size = max(2,int(len(self.agents)/subgroup_ratio))
        logging.info(f"Competition started with {len(self.agents)} agents and subgroups of size {self.subgroup_size}.")
        self.total_payoffs: dict[str, float] = {a.agent_id: 0.0 for a in self.agents}

        self.data = {a.agent_id: {"contributions": [], "punishments": [], "costs": []} for a in self.agents}

    def run_basic_round(self, alpha: float, budget: float):
        logging.info(f"Starting basic round for full set of agents with payoff factor {alpha} and budget {budget}.")
        total_payments = 0.0
        payments = {}

        for a in self.agents:
            payment = a.get_payment_basic(alpha, budget)
            logging.debug(f"Payment for agent {a.agent_id}: {payment}")
            if payment > budget:
                payment = budget
                # Log when a payment exceeds the budget
                logging.warning(f"Payment for {a.agent_id} exceeds budget. Adjusting to {budget}.")
            if payment < 0:
                payment = 0
                # Log when a payment is negative
                logging.warning(f"Negative payment for {a.agent_id}. Adjusting to 0.")
            payments[a.agent_id] = payment
            total_payments += payment

        logging.debug(f"Total payments: {total_payments}")
        for a in self.agents:
            payoff = total_payments * alpha + budget - payments[a.agent_id]
            logging.debug(f"Payoff for agent {a.agent_id} with leftover {budget - payments[a.agent_id]}: {payoff}.")
            self.total_payoffs[a.agent_id] += payoff
        self.log_results()

    def run_basic_round_subgroup(self, alpha: float, budget: float):
        logging.info(f"Starting basic round for subgroups with payoff factor {alpha} and budget {budget}.")
        all_subsets = [list(subset) for subset in itertools.combinations(self.agents, self.subgroup_size)]
        for subset in all_subsets:
            total_payments = 0.0
            payments = {}

            for a in subset:
                payment = a.get_payment_basic_subgroups(alpha, budget, self.subgroup_size, len(self.agents))
                logging.debug(f"Payment for agent {a.agent_id}: {payment}")
                if payment > budget:
                    payment = budget
                    # Log when a payment exceeds the budget
                    logging.warning(f"Payment for {a.agent_id} exceeds budget. Adjusting to {budget}.")
                if payment < 0:
                    payment = 0
                    # Log when a payment is negative
                    logging.warning(f"Negative payment for {a.agent_id}. Adjusting to 0.")
                payments[a.agent_id] = payment
                total_payments += payment

            logging.debug(f"Total payments: {total_payments}")
            for a in subset:
                payoff = total_payments * alpha + budget - payments[a.agent_id]
                logging.debug(f"Payoff for agent {a.agent_id} with leftover {budget-payments[a.agent_id]}: {payoff}.")
                self.total_payoffs[a.agent_id] += payoff
        self.log_results()

    def run_punishment_round(self, alpha: float, beta: float, budget: float):
        logging.info(f"Starting punishment round with payoff factor {alpha}, punishment factor {beta} and budget {budget}.")
        all_subsets = [list(subset) for subset in itertools.combinations(self.agents, self.subgroup_size)]
        for subset in all_subsets:
            total_payments = 0.0
            payments = {}

            for a in subset:
                payment = a.get_payment_punishment(alpha, beta, budget, self.subgroup_size, len(self.agents))
                logging.debug(f"Payment for agent {a.agent_id}: {payment}")
                if payment > budget:
                    payment = budget
                    # Log when a payment exceeds the budget
                    logging.warning(f"Payment for {a.agent_id} exceeds budget. Adjusting to {budget}.")
                if payment < 0:
                    payment = 0
                    # Log when a payment is negative
                    logging.warning(f"Negative payment for {a.agent_id}. Adjusting to 0.")
                payments[a.agent_id] = payment
                total_payments += payment

            logging.debug(f"Total payments: {total_payments}")
            average = total_payments / len(subset)
            logging.debug(f"Average payment is {average}.")
            for a in subset:
                payoff = total_payments * alpha + budget - payments[a.agent_id] - max(0, (average - payments[a.agent_id]) * beta)
                logging.debug(f"Payoff for agent {a.agent_id} with leftover {budget-payments[a.agent_id]}. Punishment {max(0, (average - payments[a.agent_id]) * beta)} -> Payoff: {payoff}. ")
                self.data[a.agent_id]["contributions"].append(payments[a.agent_id])
                self.data[a.agent_id]["punishments"].append(max(0, (average - payments[a.agent_id]) * beta))
                self.total_payoffs[a.agent_id] += payoff
        self.log_results()

    def run_discrete_round(self, alpha: float, budget: float, cost: float):
        logging.info(f"Starting discrete round with payoff factor {alpha}, cost {cost} and budget {budget}.")
        all_subsets = [list(subset) for subset in itertools.combinations(self.agents, self.subgroup_size)]
        for subset in all_subsets:
            total_payments = 0.0
            payments = {}

            for a in subset:
                payment = a.get_payment_discrete(alpha, budget, cost, self.subgroup_size, len(self.agents))
                if payment > budget:
                    payment = budget
                    # Log when a payment exceeds the budget
                    logging.warning(f"Payment for {a.agent_id} exceeds budget. Adjusting to {budget}.")
                if payment < 0:
                    payment = 0
                    # Log when a payment is negative
                    logging.warning(f"Negative payment for {a.agent_id}. Adjusting to 0.")
                payments[a.agent_id] = payment
                total_payments += payment

            logging.debug(f"Total payments: {total_payments}")
            bought_items = int(total_payments / cost)
            logging.debug(f"{bought_items} units were bought.")
            for a in subset:
                payoff = bought_items * cost * alpha + budget - payments[a.agent_id]
                self.data[a.agent_id]["contributions"].append({"payment": payments[a.agent_id], "cost": cost})
                self.data[a.agent_id]["costs"].append(cost)
                logging.debug(f"Payoff for agent {a.agent_id} with leftover {budget-payments[a.agent_id]}: {payoff}.")
                self.total_payoffs[a.agent_id] += payoff
        self.log_results()

    def log_results(self):
        # Sort agents by their total payoffs in descending order
        sorted_agents = sorted(self.agents, key=lambda ag: self.total_payoffs[ag.agent_id], reverse=True)

        logging.info("Payoffs (Sorted):")
        for i, a in enumerate(sorted_agents, 1):
            logging.info(f"{i}. {a.agent_id}: {self.total_payoffs[a.agent_id]:.2f}")

    def reset(self):
        self.total_payoffs = {a.agent_id: 0.0 for a in self.agents}
        self.data = {a.agent_id: {"contributions": [], "punishments": [], "costs": []} for a in self.agents}
        logging.info(f"Resetting payoffs \n\n")

def plot_ex2(data):
    agents = ["Group P", "Group L", "Group E"]
    colors = {'Group P': 'tab:blue', 'Group L': 'tab:orange', 'Group E': 'tab:green'}

    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(10, 4))
    for agent_id in agents:
        plt.plot(data[agent_id]["contributions"], label=f"{agent_id}", color=colors[agent_id], linewidth=2)
    plt.title("Contributions Over Rounds (Top 3)", fontsize=14)
    plt.xlabel("Round", fontsize=12)
    plt.ylabel("Contribution", fontsize=12)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(title="Agent", fontsize=10, title_fontsize=11)
    plt.tight_layout()
    plt.savefig('plots/contributions.png')

    plt.figure(figsize=(10, 4))
    for agent_id in agents:
        plt.plot(data[agent_id]["punishments"], label=f"{agent_id}", color=colors[agent_id], linewidth=2)
    plt.title("Punishments Over Rounds (Top 3)", fontsize=14)
    plt.xlabel("Round", fontsize=12)
    plt.ylabel("Punishment", fontsize=12)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(title="Agent", fontsize=10, title_fontsize=11)
    plt.tight_layout()
    plt.savefig('plots/punishments.png')

def plot_avg_payment_by_cost_bin_per_group(data, num_bins=5):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    from collections import defaultdict

    os.makedirs("plots", exist_ok=True)

    agent_ids = sorted(data.keys())
    all_costs = []

    # Gather all costs
    for entries in data.values():
        all_costs.extend(entry["cost"] for entry in entries["contributions"])

    if not all_costs:
        print("No contribution data found.")
        return

    # Dynamically determine bins
    cost_min, cost_max = min(all_costs), max(all_costs)
    bins = np.linspace(cost_min, cost_max, num_bins + 1)

    # Bin data: bin_index -> agent_id -> list of payments
    binned_payments = defaultdict(lambda: defaultdict(list))
    for agent_id, agent_data in data.items():
        for entry in agent_data["contributions"]:
            cost = entry["cost"]
            payment = entry["payment"]
            bin_idx = np.digitize(cost, bins) - 1
            bin_idx = min(bin_idx, num_bins - 1)
            binned_payments[bin_idx][agent_id].append(payment)

    # Prepare average payments per bin per group
    avg_payments_per_bin = []
    for bin_idx in range(num_bins):
        avg_per_group = []
        for agent_id in agent_ids:
            payments = binned_payments[bin_idx].get(agent_id, [])
            avg = np.mean(payments) if payments else 0
            avg_per_group.append(avg)
        avg_payments_per_bin.append(avg_per_group)

    # Plotting
    x = np.arange(num_bins)
    width = 0.8 / len(agent_ids)

    plt.figure(figsize=(12, 6))
    for i, agent_id in enumerate(agent_ids):
        values = [avg_payments_per_bin[bin_idx][i] for bin_idx in range(num_bins)]
        plt.bar(x + i * width, values, width, label=agent_id)

    bin_labels = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(num_bins)]
    plt.xticks(x + width * (len(agent_ids) - 1) / 2, bin_labels, rotation=45)
    plt.xlabel("Cost Range")
    plt.ylabel("Average Contribution")
    plt.title("Average Contribution per Group by Cost Bin")
    plt.legend(title="Agent Group")
    plt.tight_layout()
    plt.savefig("plots/avg_contributions_by_cost_bin_per_group.png")
    plt.close()

if __name__ == "__main__":
    random.seed(12345)

    logging.basicConfig(filename='competition_log.txt', level=logging.INFO,
                        format='%(message)s', filemode="w") #Change logging level to DEBUG for full output.

    competition = Competition(2.5) #Increase subgroup ratio to make subgroups smaller.

    # Run 300 rounds each:
    budget = 100

    logging.info("\n\n---- Running Ex 1 ---- \n")
    # Ex 1 a)
    for _ in range(300):
        alpha = random.uniform(0, 3)
        competition.run_basic_round(alpha=alpha, budget=budget)

    # Ex 1 b)
    for _ in range(300):
        alpha = random.uniform(0, 3)
        competition.run_basic_round_subgroup(alpha=alpha, budget=budget)

    logging.info("\n\n---- Final Result for Ex 1 ---- \n")
    competition.log_results()
    competition.reset()

    # Ex 2
    logging.info("\n\n---- Running Ex 2 ---- \n")
    for _ in range(300):
        alpha = random.uniform(0, 3)
        beta = random.uniform(0, 3)
        competition.run_punishment_round(alpha=alpha, beta=beta, budget=budget)

    logging.info("\n\n---- Final Result for Ex 2 ---- \n")
    competition.log_results()
    #plot_ex2(competition.data)
    data = competition.data
    for a in competition.agents:
        avg_payment = sum(data[a.agent_id]["contributions"]) / len(data[a.agent_id]["contributions"])
        avg_punishment =  sum(data[a.agent_id]["punishments"]) / len(data[a.agent_id]["punishments"])
        print(f"Agent {a.agent_id} - avg payment {avg_payment} average punishment {avg_punishment}.")
    competition.reset()

    #Ex 3
    logging.info("\n\n---- Running Ex 3 ---- \n")
    for _ in range(300):
        alpha = random.uniform(0, 3)
        cost = random.uniform(0.01, budget * competition.subgroup_size*1.1)
        competition.run_discrete_round(alpha=alpha, budget=budget, cost=cost)

    logging.info("\n\n---- Final Result for Ex 3 ---- \n")
    competition.log_results()
    data = competition.data
    plot_avg_payment_by_cost_bin_per_group(data, 4)
    competition.reset()

