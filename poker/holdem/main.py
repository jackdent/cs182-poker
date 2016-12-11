from poker.holdem.agents import InteractiveAgent, RandomAgent, TrainedAgent
from poker.holdem.game import HoldEmPoker
import sys
import os
import numpy as np

if __name__ == '__main__':
    BUY_IN = 10

    training_data = {}
    for line in open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'r'):
        l = line.strip().split(':')
        training_data[l[0]] = np.fromstring(l[1], dtype=float, sep=',')


    trained_wins = 0
    total_games = 0
    for _ in range(50):
        game = HoldEmPoker(TrainedAgent(BUY_IN, training_data), RandomAgent(BUY_IN))
        wins = game.play()
        trained_wins += wins[0]
        total_games += sum(wins)

    print('Trained agent won %d hands, %d%% of the total.' % (trained_wins, 100 * trained_wins / total_games))
