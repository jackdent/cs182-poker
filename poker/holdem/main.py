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
        wins = {'simple': 0, 'trained': 0}
        total_games = 100

        for i in range(total_games):
            trained_agent = TrainedAgent(BUY_IN, training_data)
            simple_agent = RandomAgent(BUY_IN)

            if i % 2 == 0:
                game = HoldEmPoker(simple_agent, trained_agent)
                winner = game.play()
                if winner == 1:
                    wins['simple'] += 1
                else:
                    wins['trained'] += 1
            else:
                game = HoldEmPoker(trained_agent, simple_agent)
                winner = game.play()
                if winner == 1:
                    wins['trained'] += 1
                else:
                    wins['simple'] += 1

        agent_1_win_rate = 100 * wins['trained'] / total_games

        print('Trained Agent won %d games out of %d, %d%% of the total.' % (wins['trained'], total_games, agent_1_win_rate))

    else:
        num_games = raw_input('How many games would you like to play?')
        try:
            for _ in range(int(num_games)):
                game = HoldEmPoker(TrainedAgent(BUY_IN, training_data), InteractiveAgent(BUY_IN))
                game.play(2000)
        except ValueError:
            print "Invalid number"
