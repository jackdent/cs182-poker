import kuhn as k

# constants
CARDS = [1, 2, 3]
PASS = 0
BET = 1
NUM_ACTIONS = 2

class Node():
	def __init__(self, infoset):
		self.infoset = infoset
		self.regretSum = [0, 0]
		self.strategy = [0, 0]
		self.strategySum = [0, 0]

	def getStrategy(self, weight):
		normalizingSum = 0
		for i in range(NUM_ACTIONS):
			if regretSum[i] > 0:
				self.strategy[0]

	def getAverageStrategy(self):


class KuhnTrainer():
	def __init__(self, iterations):
		self.iterations = iterations

	def train(self):
		util = 0
		for _ in range(self.iterations):
			util += self.cfr(CARDS, "", 1, 1)

	def cfr(cards, history, agent, p0, p1):
		plays = len(history)
		player = plays % 2
		opponent = 1 - player

		if plays > 1:
			isPlayerCardHigher = cards[player] > cards[opponent]
			terminalPass = history[-1] == 0
			doubleBet = history[-1] == 1 and history[-2] == 1

			if terminalPass:
				if history == [0, 0]:
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


if __name__ == '__main__':
    BUY_IN = 10
    game = k.KuhnPoker(k.InteractiveAgent(BUY_IN), k.SimpleAgent(BUY_IN))
    game.play()
