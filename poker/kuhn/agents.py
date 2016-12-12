import random

from poker.kuhn.game import CARDS, KuhnAction


class KuhnAgent(object):
    def __init__(self, stack_size):
        self.stack_size = stack_size

    def choose_action(self):
        raise NotImplementedError

class NashAgent(KuhnAgent):
    def choose_action(self, game_state):
        if random.random() < 1/3:
            return KuhnAction.BET
        else:
            return KuhnAction.PASS


class SimpleAgent(KuhnAgent):
    def choose_action(self, game_state):
        card, _ = game_state

        if card == CARDS[-1] or random.random() < 1/4:
            return KuhnAction.BET
        else:
            return KuhnAction.PASS


class TrainedAgent(KuhnAgent):
    def __init__(self, stack_size, training_data):
        super(TrainedAgent, self).__init__(stack_size)
        self.training_data = training_data

    def choose_action(self, game_state):
        card, history = game_state
        infoset = str(card) + ''.join(history)
        # strategy = self.training_data[infoset].getAverageStrategy()
        strategy = []
        if infoset in self.training_data:
            strategy = self.training_data[infoset]
        else:
            strategy = [1/len(KuhnAction.ALL)] * len(KuhnAction.ALL)

        # print "%s:%s" % (infoset, strategy)

        r = random.random()
        cumulative_probability = 0
        a = 0

        while (a < len(KuhnAction.ALL) - 1):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                break
            a += 1

        return KuhnAction.ALL[a]


class InteractiveAgent(KuhnAgent):
    def choose_action(self, game_state):
        card, history = game_state

        while True:
            if len(history) > 0 and history[-1] == 'b':
                action = raw_input('Your card is %d, you have %d chips remaining, and Agent 2 bet. '
                                   'Enter "p" to pass or "b" to bet: ' % (card, self.stack_size))
            else:
                action = raw_input('Your card is %d and you have %d chips remaining. Enter '
                                   '"p" to pass or "b" to bet: ' % (card, self.stack_size))

            if action == 'p':
                return KuhnAction.PASS
            elif action == 'b':
                return KuhnAction.BET
            else:
                print('Unknown action "%s", please try again.' % action)
