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
