from poker.holdem.agents import InteractiveAgent, RandomAgent, TrainedAgent
from poker.holdem.game import HoldEmPoker
import sys
import os
import numpy as np
import argparse
import zipfile

if __name__ == '__main__':
    BUY_IN = 10

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', dest='test', action='store_true')
    test = parser.parse_args().test

    print "Loading training data...."
    training_data = {}
    with zipfile.ZipFile(os.path.join(os.path.dirname(__file__), 'strategies','ten_card_strategy.txt.zip')) as z:
        with z.open(z.infolist()[0]) as f:
            for line in f:
                l = line.strip().split(':')
                training_data[l[0]] = np.fromstring(l[1], dtype=float, sep=',')

    if test:
        trained_wins = 0
        total_hands = 0
        get_agent = {'Random': lambda x: RandomAgent(x), 'Trained': lambda x: TrainedAgent(x, training_data)}
        players = ['Trained','Random']
        for i in range(50):
            game = HoldEmPoker(get_agent[players[0]](BUY_IN),get_agent[players[1]](BUY_IN))
            wins = game.play()
            trained_wins += wins[i%2]
            total_hands += sum(wins)
            players.reverse()

        print('Trained agent won %d hands, %d%% of the total.' % (trained_wins, 100 * trained_wins / total_hands))

    else:
        num_games = raw_input('How many games would you like to play?')
        try:
            for _ in range(int(num_games)):
                game = HoldEmPoker(TrainedAgent(BUY_IN, training_data), InteractiveAgent(BUY_IN))
                game.play(2000)
        except ValueError:
            print "Invalid number"