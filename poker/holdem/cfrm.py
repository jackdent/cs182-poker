import csv
import os
import random
import time
import argparse

from deuces import Card, Deck, Evaluator
from poker.holdem.game import HoldEmAction, DECK
from poker.common import Node, Trainer

class HoldemTrainer(Trainer):
    def getCards(self, i, n_shards):
        max_search_iter = n_shards*5
        for _ in range(max_search_iter):
            random.shuffle(DECK)
            # Sort the 3 starting board cards because their order doesn't matter
            starting_board = DECK[:3]
            starting_board.sort()
            if (abs(hash(str(starting_board)))) % n_shards == i:
                return starting_board+DECK[3:5], [DECK[5:7], DECK[7:9]]
        return None, None

    def train(self, i, n_shards, strategy_folder):
        util = 0
        start_time = time.time()

        for _ in range(self.iterations):
            board, hands = self.getCards(i, n_shards)
            if board and hands:
                util += self.cfr((board, [], ""), hands, 1, 1)
            else:
                print "Did not find a good hash"
                return

        print 'Average time per iteration:'
        print ((time.time() - start_time)/(self.iterations))

        print 'Average game value: %f' % (util / (self.iterations))

        with open(os.path.join(os.path.dirname(__file__), 'strategies', strategy_folder, 'strategy_%d.txt'%(i)), 'w') as f:
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

    # Command line arguments to specify parameters for sharding / saving
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', help='Job number', type=int, default=0)
    parser.add_argument('--n_shards', help='Total number of shards/jobs', type=int, default=199)
    parser.add_argument('--n_iterations', help='Number of iterations per shard, (should be more than \
                         the number of boards hash to a given shard, the more the better)', type=int, default=1)
    parser.add_argument('--strategy_folder', help='The folder to save the strategy files in', default='ten_cards')
    parser.add_argument('--starting_job', help='Starting index of the first job', type=int, default=0)

    i = parser.parse_args().i
    n_shards = parser.parse_args().n_shards
    n_iterations = parser.parse_args().n_iterations
    strategy_folder = parser.parse_args().strategy_folder

    # Odyssey doesn't let you run an array of jobs that doesn't start at 0
    # so this is a hack to let you start your array at job i
    starting_job = parser.parse_args().starting_job
    i += starting_job

    h = HoldemTrainer(n_iterations)
    h.train(i, n_shards, strategy_folder)
