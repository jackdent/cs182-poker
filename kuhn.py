import random
import numpy as np

# Jack, Queen and King, respectively
CARDS = [1, 2, 3]
ACTIONS = ['p', 'b']
NUM_ACTIONS = 2

class Action(object):
    PASS, BET = range(2)


class Agent(object):
    def __init__(self, stack_size):
        self.stack_size = stack_size

    def choose_action(self):
        raise NotImplementedError


class BetAgent(Agent):
    def choose_action(self, game_state):
        return Action.BET


class NashAgent(Agent):
    def choose_action(self, game_state):
        if random.randon() < (1/3):
            return Action.BET
        else:
            return Action.PASS

class SimpleAgent(Agent):
    def choose_action(self, game_state):
        card, _, _, _, _ = game_state
        if card == CARDS[-1] or random.random() < 0.25:
            return Action.BET
        else:
            return Action.PASS

class TrainedAgent(Agent):
    def __init__(self, stack_size, training_data):
        super(TrainedAgent, self).__init__(stack_size)
        self.training_data = training_data

    def choose_action(self, game_state):
        card, history, _, _, _ = game_state
        infoset = str(card) + history
        # strategy = self.training_data[infoset].getAverageStrategy()
        strategy = self.training_data[infoset]
        print "%s:%s" % (infoset, strategy)
        r = random.random()
        cumulative_probability = 0
        a = 0
        while (a < NUM_ACTIONS - 1):
            cumulative_probability += strategy[a]
            if r < cumulative_probability:
                break
            a += 1

        return a

class InteractiveAgent(Agent):
    def choose_action(self, game_state):
        card, history, _, _, _ = game_state
        while True:
            if len(history) > 0 and history[-1] == 'b':
                action = raw_input('Your card is %d, you have %d chips remaining, and Agent 2 bet. Enter '
                               '"p" to pass or "b" to bet: ' % (card, self.stack_size))
            else:
                action = raw_input('Your card is %d and you have %d chips remaining. Enter '
                               '"p" to pass or "b" to bet: ' % (card, self.stack_size))

            if action == 'p':
                return Action.PASS
            elif action == 'b':
                return Action.BET
            else:
                print('Unknown action "%s", please try again.' % action)


class KuhnPoker(object):
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, max_hands=1000):
        hands = 0
        while self.agent_1.stack_size > 0 and self.agent_2.stack_size > 0 and hands < max_hands:
            winner = self.play_hand()
            winning_agent = 1 if winner is self.agent_1 else 2

            print('Agent %d won the hand. Agents 1 and 2 now have %d and %d chips, respectively.'
                  % (winning_agent, self.agent_1.stack_size, self.agent_2.stack_size))

            hands += 1

    def play_hand(self):
        pot = 0

        # Collect blinds
        for agent in (self.agent_1, self.agent_2):
            assert agent.stack_size > 0
            agent.stack_size -= 1
            pot += 1

        # Give a card to each player
        shuffled_cards = random.sample(CARDS, 2)
        cards = {self.agent_1: shuffled_cards[0], self.agent_2: shuffled_cards[1]}

        # Allow agents to bet in rounds until the end of the hand
        history = ''
        agents = [self.agent_1, self.agent_2]
        winner = None

        while winner is None:
            current_agent, prev_agent = agents
            game_state = (cards[current_agent], history, pot, self.agent_1.stack_size, self.agent_2.stack_size)

            if current_agent.stack_size == 0:
                action = Action.PASS
            else:
                action = current_agent.choose_action(game_state)

                if action == Action.BET:
                    current_agent.stack_size -= 1
                    pot += 1

            if len(history) > 0:
                prev_action = history[-1]

                if prev_action == ACTIONS[action]:
                    winner = max(cards, key=cards.get)
                elif prev_action == 'b' and ACTIONS[action] == 'p':
                    winner = prev_agent

            history += ACTIONS[action]
            agents.reverse()

        winner.stack_size += pot
        return winner


if __name__ == '__main__':
    BUY_IN = 100
    user_input = raw_input('Select which agent should be used. Default is simple, i for interactive, t for trained, n for nash: ')

    f = open('strategy.py', 'r')

    data = {}
    for line in f:
        l = line.strip().split(':')
        strategy = np.fromstring(l[1], dtype=float, sep=',')
        data[l[0]] = strategy

    agent = SimpleAgent(BUY_IN)
    if user_input == 'i':
        agent = InteractiveAgent(BUY_IN)
    elif user_input == 't':
        agent = TrainedAgent(BUY_IN, data)

    game = KuhnPoker(agent, TrainedAgent(BUY_IN, data))
    game.play(2000)

