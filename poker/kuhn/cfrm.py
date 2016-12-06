import csv
import os
import random

from poker.kuhn.game import CARDS, KuhnAction
from poker.common import Node, Trainer

# constants
PASS = 0
BET = 1

class KuhnTrainer(Trainer):
	def train(self):
		util = 0
		for _ in range(self.iterations):
			shuffled_cards = random.sample(CARDS, 2)
			util += self.cfr("", shuffled_cards, 1, 1)

		print 'Average game value: %f' % (util / self.iterations)

		with open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'w') as f:
			for k, v in self.nodeMap.iteritems():
				print v.toString()
				f.write(v.toString() + '\n')

	def cfr(self, history, cards, p0, p1):
		plays, player, opponent = self.getPlayers(history)

		# Check if in a terminal state
		if plays > 1:
			isPlayerCardHigher = cards[player] > cards[opponent]
			terminalPass = history[-1] == 'p'
			doubleBet = history[-2:] == 'bb'

			# Current player wins if other player passed and current didn't (or if better card)
			if terminalPass:
				return 1 if history != 'pp' or isPlayerCardHigher else -1
			elif doubleBet:
				return 2 if isPlayerCardHigher else -2

		infoset = str(cards[player]) + history
		node = self.getNode(infoset, KuhnAction.ALL)

		return self.computeStrategyAndRegrets(KuhnAction.ALL, cards, player, node, history, p0, p1)

	def nextState(self, state, action):
		return state+action

if __name__ == '__main__':
	k = KuhnTrainer(1000)
	k.train()
