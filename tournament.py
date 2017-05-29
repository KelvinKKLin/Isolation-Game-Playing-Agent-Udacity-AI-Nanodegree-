"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

NUM_MATCHES = 5  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

        if termination == "timeout":
            timeout_count += 1
        elif winner not in test_agents and termination == "forfeit":
            forfeit_count += 1

    return timeout_count, forfeit_count


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches, l):

    #Whether an agent had over 70% win rate
    over70 = False
    paramsForMaxAgentOver70 = ""
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)

    l.write("\n{:^9}{:^13}{:^13}{:^13}{:^13}{:^13}{:^13}\n".format(
        "Match #", "Opponent", test_agents[0].name, test_agents[1].name,
        test_agents[2].name, test_agents[3].name, test_agents[4].name))
    l.write("{:^9}{:^13} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5}\n"
          .format("", "", *(["Won", "Lost"] * 5)))

    for idx, agent in enumerate(cpu_agents):
        wins = {test_agents[0].player: 0,
                test_agents[1].player: 0,
                test_agents[2].player: 0,
                test_agents[3].player: 0,
                test_agents[4].player: 0,
                agent.player: 0}

        l.write("{!s:^9}{:^13}\n".format(idx + 1, agent.name))

        counts = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += counts[0]
        total_forfeits += counts[1]
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        l.write(" {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5} {:^5}| {:^5}\n"
              .format(*round_totals))

    l.write("-" * 74 + "\n")
    l.write("{:^9}{:^13}{:^13}{:^13}{:^13}{:^13}\n".format(
        "", "Win Rate:",
        *["{:.1f}%".format(100 * total_wins[a.player] / total_matches)
          for a in test_agents]
    ))

    print("GAME FINISHED")

    #Genetic algorithm
    win_rate = []
    top3agents = []
    for a in test_agents:
        win_rate.append(100 * total_wins[a.player] / total_matches)

    maxAgentWinRate = float("-inf")
    win_rate.sort()
    for a in test_agents:
        agentWinRate = 100 * total_wins[a.player] / total_matches
        if (agentWinRate >= 70) and (agentWinRate > maxAgentWinRate):
            maxAgentWinRate = agentWinRate
            over70 = True
        if (agentWinRate == win_rate[-1]) or (agentWinRate == win_rate[-2]) or (agentWinRate == win_rate[-3]):
            top3agents.append(a)

    #Crossover
    new_param1 = []
    new_param2 = []

    for i in range(5):
        parent1 = random.randrange(0, 3)
        parent2 = random.randrange(0, 3)
        new_params1.append(top3agents[parent1].getParams()[i])
        new_params2.append(top3agents[parent2].getParams()[i])

    #Mutation
    for i in range(5):
        mutationRate1 = random.random()
        mutationRate2 = random.random()
        if mutationRate1 < 0.1:
            new_params1[i] = random.gauss(0, 10)
        if mutationRate2 < 0.1:
            new_params2[i] = random.gauss(0, 10)

    return top3agents[0].getParams(), top3agents[1].getParams(), top3agents[2].getParams(), new_param1, new_param2, over70, maxAgentWinRate

def main():

    f = open('C:/Users/Owner/Desktop/ga_results.txt', 'w')
    l = open('C:/Users/Owner/Desktop/ga_log.txt', 'w')

    #Parameters for genetic algorithm
    params1 = [random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10)]
    params2 = [random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10)]
    params3 = [random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10)]
    params4 = [random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10), random.gauss(0, 10)]
    params5 = [0.2, 0.2, 0.2, 0.2, 0.2]
    iteration = 1

    try:
        while True:
            print("Running Iteration: " + str(iteration))
            l.write("ITERATION: " + str(iteration) + "\n")
            iteration = iteration+1

            l.write("PARAMETER 1: " + str(params1) + "\n")
            l.write("PARAMETER 2: " + str(params2) + "\n")
            l.write("PARAMETER 3: " + str(params3) + "\n")
            l.write("PARAMETER 4: " + str(params4) + "\n")
            l.write("PARAMETER 5: " + str(params5) + "\n")
            l.write("---------------------------------\n")

            # Define two agents to compare -- these agents will play from the same
            # starting position against the same adversaries in the tournament
            test_agents = [
                Agent(AlphaBetaPlayer(score_fn=custom_score_3, params=params1), "Agent_1"),
                Agent(AlphaBetaPlayer(score_fn=custom_score_3, params=params2), "Agent_2"),
                Agent(AlphaBetaPlayer(score_fn=custom_score_3, params=params3), "Agent_3"),
                Agent(AlphaBetaPlayer(score_fn=custom_score_3, params=params4), "Agent_4"),
                Agent(AlphaBetaPlayer(score_fn=custom_score_3, params=params5), "Agent_5")
            ]

            # Define a collection of agents to compete against the test agents
            cpu_agents = [
                Agent(RandomPlayer(), "Random"),
                Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
                Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
                Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
                Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
                Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
                Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
            ]

            l.write("{:^74}\n".format("*************************"))
            l.write("{:^74}\n".format("Playing Matches"))
            l.write("{:^74}\n".format("*************************"))
            p1, p2, p3, p4, p5, o70, mawr = play_matches(cpu_agents, test_agents, NUM_MATCHES, l)

            params1 = p1
            params2 = p2
            params3 = p3
            params4 = p4
            params5 = p5

            if o70:
                f.write(str(mwar) + '\n')

    except KeyboardInterrupt:
        f.close()
        l.close()

    #except:
    #    f.close()
    #    print("An Error Occured")

if __name__ == "__main__":
    main()
