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
