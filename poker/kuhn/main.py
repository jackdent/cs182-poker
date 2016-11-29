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

    game = KuhnPoker(agent, TrainedAgent(BUY_IN, training_data))
    game.play(2000)
