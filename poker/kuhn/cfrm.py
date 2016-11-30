import csv
import os
import random

from poker.kuhn.game import CARDS, KuhnAction
from poker.common import Node

# constants
PASS = 0
BET = 1

class KuhnTrainer():
	def __init__(self, iterations):
		self.iterations = iterations
		self.nodeMap = {}

	def train(self):
		util = 0
		for _ in range(self.iterations):
			shuffled_cards = random.sample(CARDS, 2)
			util += self.cfr(shuffled_cards, "", 1, 1)

		print 'Average game value: %f' % (util / self.iterations)

		with open(os.path.join(os.path.dirname(__file__), 'strategy.txt'), 'w') as f:
			for k, v in self.nodeMap.iteritems():
				print v.toString()
				f.write(v.toString() + '\n')

	def cfr(self, cards, history, p0, p1):
		nodeUtil = 0
		plays = len(history)
		player = plays % 2
		opponent = 1 - player

		# Check if in a terminal state
		if plays > 1:
			isPlayerCardHigher = cards[player] > cards[opponent]
			terminalPass = history[-1] == 'p'
			doubleBet = history[-2:] == 'bb'

			if terminalPass:
				if history == 'pp':
					if isPlayerCardHigher:
						return 1
					else:
						return -1
				else:
					return 1
			elif doubleBet:
				if isPlayerCardHigher:
					return 2
				else:
					return -2

		infoset = str(cards[player]) + history
		node = None

		# Retrieve corresponding state from dictionary
		if infoset in self.nodeMap:
			node = self.nodeMap[infoset]
		else:
			node = Node(infoset, len(KuhnAction.ALL))
			self.nodeMap[infoset] = node

		strategy = []
		util = [0] * len(KuhnAction.ALL)

		# Recursively compute strategy

		strategy = node.getStrategy(p0) if player == 0 else node.getStrategy(p1)

		for a in range(len(KuhnAction.ALL)):
			nextHistory = history + 'p' if a == PASS else history + 'b'

			if player == 0:
				util[a] = -self.cfr(cards, nextHistory, p0 * strategy[a], p1)
			else:
				util[a] = -self.cfr(cards, nextHistory, p0, p1 * strategy[a])
			nodeUtil += strategy[a] * util[a]

		# Compute regrets
		for a in range(len(KuhnAction.ALL)):
			regret = util[a] - nodeUtil
			node.regretSum[a] += p1 * regret if player == 0 else p0 * regret

		# self.nodeMap[infoset] = node

		return nodeUtil


if __name__ == '__main__':
	k = KuhnTrainer(1000000)
	k.train()
