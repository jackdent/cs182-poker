import csv
import os
import random

from deuces import Card, Deck, Evaluator
from poker.holdem.game import HoldEmAction
from poker.common import Node, Trainer

# Fixed board and reduced deck -- just for very simple testing
board=[147715, 268471337, 8398611, 2131213, 2102541]
ten_cards = [135427, 529159,268454953,16787479,67119647,16795671,69634,268446761,139523,16812055]
six_cards = [135427, 529159,268454953,16787479,67119647,16795671]

class HoldemTrainer(Trainer):

    def train(self):
        util = 0

        for _ in range(self.iterations):
            """
            deck = Deck()
            hands = [deck.draw(2), deck.draw(2)]
            board = deck.draw(5)
            """
            
            # THIS IS JUST FOR TESTING TO REDUCE SPACE
            hand_cards = random.sample(ten_cards,4)
            hands = [hand_cards[:2], hand_cards[2:]]

            util += self.cfr((board, [], ""), hands, 1, 1)

        print 'Average game value: %f' % (util / (self.iterations))

        with open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'w') as f:
            for k, v in self.nodeMap.iteritems():
                f.write(v.toString() + '\n')


    def cfr(self, (board, history, round_history), cards, p0, p1):
        # Set up variables
        hist = list(history)
        round_hist = str(round_history)
        full_history = ''.join(history)+round_hist
        visible_board = board[:3+len(hist)]

        plays, player, opponent = self.getPlayers(full_history)

        possible_actions = HoldEmAction.possible_actions(round_hist)
        # Possible actions returns ['c','b','f'] any time it's called with an empty string,
        # except for the first time. This is a shady solution-- fix later
        if plays == 0:
            possible_actions = HoldEmAction.possible_actions('c')
         
        # Check if it is the end of a round
        if len(possible_actions) == 0:
            evaluator = Evaluator()
            scores = [evaluator.evaluate(visible_board, hand) for hand in cards]
            isPlayerHandBetter = scores[player] < scores[opponent]
            winnings = 1 + (''.join(full_history).count('b'))/2
            terminalFold = (round_hist[-1] == 'f')

            # If last player folded, current player automatically wins
            if terminalFold:
                return winnings
            # If there are no more rounds, give points to player with better cards
            elif len(hist) == 2:
                return winnings if isPlayerHandBetter else -winnings

            # Start a new round
            hist.append(round_hist)
            round_hist=''
            visible_board = board[:3+len(hist)]
            possible_actions = HoldEmAction.possible_actions('c')

        # Retrieve corresponding state from dictionary
        infoset = str(visible_board)+str(cards[player]) + full_history
        node = self.getNode(infoset, possible_actions)

        return self.computeStrategyAndRegrets(possible_actions, cards, player, node,
                                                (board, hist, round_hist), p0, p1)

    def nextState(self, infoset, action):
        board, history, round_history = infoset
        return (board, history, round_history + action)

if __name__ == '__main__':
    h = HoldemTrainer(10)
    h.train()
