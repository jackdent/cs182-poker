import csv
import os
import random

from deuces import Card, Deck, Evaluator
from poker.holdem.game import HoldEmAction
from poker.common import Node

# Fixed board and reduced deck -- just for very simple testing
board=[147715, 268471337, 8398611, 2131213, 2102541]
ten_cards = [135427, 529159,268454953,16787479,67119647,16795671,69634,268446761,139523,16812055]
six_cards = [135427, 529159,268454953,16787479,67119647,16795671]

class HoldemTrainer():
    def __init__(self, iterations):
        self.iterations = iterations
        self.nodeMap = {}

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

            util += self.cfr(board, hands, [], "", 1, 1)

        print 'Average game value: %f' % (util / (self.iterations))

        with open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'w') as f:
            for k, v in self.nodeMap.iteritems():
                f.write(v.toString() + '\n')


    def cfr(self, board, cards, history, round_history, p0, p1):
        # Set up variables
        current_history = list(history)
        new_round_history = str(round_history)
        full_history = ''.join(history)+round_history
        visible_board = board[:3+len(current_history)]

        plays = len(full_history)
        player = plays % 2
        opponent = 1 - player

        possibleActions = HoldEmAction.possible_actions(round_history)
        # Possible actions returns ['c','b','f'] any time it's called with an empty string,
        # except for the first time. This is a shady solution-- fix later
        if plays == 0:
            possibleActions = HoldEmAction.possible_actions('c')
         
        # Check if it is the end of a round
        if len(possibleActions) == 0:
            evaluator = Evaluator()
            scores = [evaluator.evaluate(visible_board, hand) for hand in cards]
            isPlayerHandBetter = scores[player] < scores[opponent]
            winnings = 1 + (''.join(full_history).count('b'))/2
            terminalFold = (new_round_history[-1] == 'f')

            # If last player folded, current player automatically wins
            if terminalFold:
                return winnings
            # If there are no more rounds, give points to player with better cards
            elif len(current_history) == 2:
                if isPlayerHandBetter:
                    return winnings
                else:
                    return -winnings

            # Start a new round
            current_history.append(new_round_history)
            new_round_history=''
            visible_board = board[:3+len(current_history)]
            possibleActions = HoldEmAction.possible_actions('c')

        # Retrieve corresponding state from dictionary
        infoset = str(visible_board)+str(cards[player]) + full_history
        node = None
        nodeUtil = 0
        if infoset in self.nodeMap:
            node = self.nodeMap[infoset]
        else:
            node = Node(infoset, len(possibleActions))
            self.nodeMap[infoset] = node

        strategy = []
        util = [0] * len(possibleActions)

        # Recursively compute strategy
        if player == 0:
            strategy = node.getStrategy(p0)
        else:
            strategy = node.getStrategy(p1)

        for action_idx, action in enumerate(possibleActions):
            next_round_history = new_round_history + action

            if player == 0:
                util[action_idx] = -self.cfr(board, cards, current_history,
                                            next_round_history, p0 * strategy[action_idx], p1)
            else:
                util[action_idx] = -self.cfr(board, cards, current_history,
                                            next_round_history, p0, p1 * strategy[action_idx])

            nodeUtil += strategy[action_idx] * util[action_idx]

        # Compute regrets
        for a in range(len(possibleActions)):
            regret = util[a] - nodeUtil
            if player == 0:
                node.regretSum[a] += p1 * regret
            else:
                node.regretSum[a] += p0 * regret

        return nodeUtil


if __name__ == '__main__':
    h = HoldemTrainer(800)
    h.train()
