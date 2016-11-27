import kuhn as k
import random

# constants
CARDS = [1, 2, 3]
PASS = 0
BET = 1
NUM_ACTIONS = 2
nodeMap = {}

class Node():
	def __init__(self, infoset):
		self.infoset = infoset
		self.regretSum = [0, 0]
		self.strategy = [0, 0]
		self.strategySum = [0, 0]

	def getStrategy(self, weight):
		normalizingSum = 0
		for a in range(NUM_ACTIONS):
			if self.regretSum[a] > 0:
				self.strategy[a] = self.regretSum[a]
			else:
				self.strategy[a] = 0
			normalizingSum += self.strategy[a]

		for a in range(NUM_ACTIONS):
			if normalizingSum > 0:
				self.strategy[a] /= normalizingSum
			else:
				self.strategy[a] = 1.0/NUM_ACTIONS

			self.strategySum[a] += weight * self.strategy[a]

		return self.strategy

	def getAverageStrategy(self):
		avgStrategy = [0, 0]
		normalizingSum = 0

		for a in range(NUM_ACTIONS):
			normalizingSum += self.strategySum[a]
		for a in range(NUM_ACTIONS):
			if normalizingSum > 0:
				avgStrategy[a] = self.strategySum[a]/normalizingSum
			else:
				avgStrategy[a] = 1.0/NUM_ACTIONS

		return avgStrategy

	def toString(self):
		avgStrategy = self.getAverageStrategy()
		', '.join([str(x) for x in avgStrategy])
		return ('%s: %s' % (self.infoset, avgStrategy))


class KuhnTrainer():
	def __init__(self, iterations):
		self.iterations = iterations
	
	def train(self):
		util = 0
		for _ in range(self.iterations):
			shuffled_cards = random.sample(CARDS, 2)
			util += self.cfr(shuffled_cards, "", 1, 1)

		print 'Average game value: %f' % (util / self.iterations)

		for k, v in nodeMap.iteritems():
			print v.toString()

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
		if infoset in nodeMap:
			node = nodeMap[infoset]
		else:
			node = Node(infoset)
			nodeMap[infoset] = node

		strategy = []
		util = [0, 0]

		# Recursively compute strategy
		if player == 0:
			strategy = node.getStrategy(p0)
		else:
			strategy = node.getStrategy(p1)

		for a in range(NUM_ACTIONS):
			if a == PASS:
				nextHistory = history + 'p'
			else:
				nextHistory = history + 'b'

			if player == 0:
				util[a] = self.cfr(cards, nextHistory, p0 * strategy[a], p1)
			else:
				util[a] = self.cfr(cards, nextHistory, p0, p1 * strategy[a])
			nodeUtil += strategy[a] * util[a]

		# Compute regrets
		for a in range(NUM_ACTIONS):
			regret = util[a] - nodeUtil
			if player == 0:
				node.regretSum[a] += p1 * regret
			else:
				node.regretSum[a] += p0 * regret

		nodeMap[infoset] = node

		return nodeUtil


if __name__ == '__main__':
	k = KuhnTrainer(10000)
	k.train()
    #BUY_IN = 10
    #game = k.KuhnPoker(k.InteractiveAgent(BUY_IN), k.SimpleAgent(BUY_IN))
    #game.play()
