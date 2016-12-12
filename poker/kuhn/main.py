import os
import numpy as np
import sys

from poker.kuhn.agents import InteractiveAgent, TrainedAgent, NashAgent, SimpleAgent
from poker.kuhn.game import KuhnPoker

if __name__ == '__main__':
    BUY_IN = 100

    training_data = {}
    for line in open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'r'):
        l = line.strip().split(':')
        training_data[l[0]] = np.fromstring(l[1], dtype=float, sep=',')

    user_agent = raw_input('Select which agent should be used. Default is simple, i for '
                           'interactive, t for trained, n for nash, s for simple: ')
    if user_agent == 'i':
        agent = InteractiveAgent(BUY_IN)
    elif user_agent == 't':
        agent = TrainedAgent(BUY_IN, training_data)
    elif user_agent == 'n':
        agent = NashAgent(BUY_IN)
    elif user_agent == 's':
        agent = SimpleAgent(BUY_IN)
    else:
        print('Invalid agent "%s".' % user_agent)
        sys.exit()

    wins = {'simple': 0, 'trained': 0}
    total_games = 100

    for i in range(total_games):
        trained_agent = TrainedAgent(BUY_IN, training_data)
        simple_agent = SimpleAgent(BUY_IN)

        if i % 2 == 0:
            game = KuhnPoker(simple_agent, trained_agent)
            winner = game.play()
            if winner == 1:
                wins['simple'] += 1
            else:
                wins['trained'] += 1
        else:
            game = KuhnPoker(trained_agent, simple_agent)
            winner = game.play()
            if winner == 1:
                wins['trained'] += 1
            else:
                wins['simple'] += 1

    agent_1_win_rate = 100 * wins['trained'] / total_games

    print('Trained Agent won %d games out of %d, %d%% of the total.' % (wins['trained'], total_games, agent_1_win_rate))
