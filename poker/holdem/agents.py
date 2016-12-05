from deuces import Card
import random

from poker.holdem.game import HoldEmAction


class HoldEmAgent(object):
    def __init__(self, stack_size):
        self.stack_size = stack_size

    def choose_action(self, game_state, possible_actions):
        raise NotImplementedError


class RandomAgent(HoldEmAgent):
    def choose_action(self, game_state, possible_actions):
        return random.choice(possible_actions)


class InteractiveAgent(HoldEmAgent):
    def choose_action(self, game_state, possible_actions):
        while True:
            board, hand, _, _ = game_state

            print('Your hand is:')
            Card.print_pretty_cards(hand)
            print('You have %d chips remaining.' % self.stack_size)

            filtered = ['"%s" to %s' % (k, v) for k, v in HoldEmAction.DESCRIPTIONS.iteritems()
                                              if k in possible_actions]
            action = raw_input('Enter %s: ' % ', '.join(filtered))

            if action == 'f':
                return HoldEmAction.FOLD
            elif action == 'c':
                return HoldEmAction.CHECK
            elif action == 'b':
                return HoldEmAction.BET
            else:
                print('Unknown action "%s", please try again.' % action)

class TrainedAgent(HoldEmAgent):
    def __init__(self, stack_size, training_data):
        super(TrainedAgent, self).__init__(stack_size)
        self.training_data = training_data

    def choose_action(self, game_state, possible_actions):
        visible_board, cards, history, round_history = game_state

        full_history = ''.join([action for r in history for action in r]+round_history)
        
        infoset = str(visible_board)+str(cards)+ full_history
        strategy = self.training_data[infoset]
        #print "%s:%s" % (infoset, strategy)

        r = random.random()
        cumulative_probability = 0
        a = 0

        while (a < len(possible_actions) - 1):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                break
            a += 1

        return possible_actions[a]
