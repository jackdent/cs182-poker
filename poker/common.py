import collections


class BannerPrinter(object):
    def __init__(self, token='=', repeat=40):
        self.token = token
        self.repeat = repeat

    def __enter__(self):
        print(self.token * self.repeat)

    def __exit__(self, *exc):
        print(self.token * self.repeat)


def Tree():
    return collections.defaultdict(Tree)


class Action(object):
    @classmethod
    def possible_actions(cls, partial_history):
        current_node = cls.VALID_ACTIONS

        for action in partial_history:
            current_node = current_node[action]

            if current_node is True or len(current_node) == 0:
                return []

        return current_node.keys()

class Node():
    def __init__(self, infoset, numActions):
        self.numActions = numActions
        self.infoset = infoset
        self.regretSum = [0] * numActions
        self.strategy = [0] * numActions
        self.strategySum = [0] * numActions

    def getStrategy(self, weight):
        normalizingSum = 0
        for a in range(self.numActions):
            if self.regretSum[a] > 0:
                self.strategy[a] = self.regretSum[a]
            else:
                self.strategy[a] = 0
            normalizingSum += self.strategy[a]

        for a in range(self.numActions):
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / self.numActions

            self.strategySum[a] += weight * self.strategy[a]

        return self.strategy

    def getAverageStrategy(self):
        avgStrategy = [0] * self.numActions
        normalizingSum = 0

        for a in range(self.numActions):
            normalizingSum += self.strategySum[a]
        for a in range(self.numActions):
            if normalizingSum > 0:
                avgStrategy[a] = self.strategySum[a]/normalizingSum
            else:
                avgStrategy[a] = 1.0 / self.numActions

        return avgStrategy

    def toString(self):
        avgStrategy = self.getAverageStrategy()
        str_strategy = ', '.join([str(x) for x in avgStrategy])
        return ('%s:%s' % (self.infoset, str_strategy))
