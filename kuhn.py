import random

# Jack, Queen and King, respectively
CARDS = [1, 2, 3]
ACTIONS = ['p', 'b']

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


class SimpleAgent(Agent):
    def choose_action(self, game_state):
        card, _, _, _, _ = game_state
        if card == CARDS[-1] or random.random() < 0.25:
            return Action.BET
        else:
            return Action.PASS


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
    BUY_IN = 10
    game = KuhnPoker(InteractiveAgent(BUY_IN), SimpleAgent(BUY_IN))
    game.play()

