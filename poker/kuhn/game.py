import random

from poker.common import Action, BannerPrinter, Tree

# Jack, Queen and King, respectively
CARDS = [1, 2, 3]

class KuhnAction(Action):
    ALL = PASS, BET = 'p', 'b'

    VALID_ACTIONS = Tree()
    VALID_ACTIONS[PASS][PASS] = True
    VALID_ACTIONS[PASS][BET][PASS] = True
    VALID_ACTIONS[PASS][BET][BET] = True
    VALID_ACTIONS[BET][PASS] = True
    VALID_ACTIONS[BET][BET] = True


class KuhnPoker(object):
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, max_hands=1000):
        wins = [0, 0]

        while self.agent_1.stack_size > 1 and self.agent_2.stack_size > 1 and sum(wins) < max_hands:
            # An agent must have at least 2 chips to enter a hand (otherwise) the opponent
            # can win trivially, by betting.
            winner = self.play_hand()
            winning_agent = 1 if winner is self.agent_1 else 2

            # with BannerPrinter():
            #     print('Agent %d won the hand. Agents 1 and 2 now have %d and %d chips, respectively.'
            #           % (winning_agent, self.agent_1.stack_size, self.agent_2.stack_size))

            wins[winning_agent - 1] += 1

        agent_1_win_rate = 100 * wins[0] / max_hands
        print('Agent 1 won %d hands, %d%% of the total.' % (wins[0], agent_1_win_rate))

        return 1 if agent_1_win_rate > 50 else 2

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
        history = []
        possible_actions = KuhnAction.possible_actions(history)
        agents = [self.agent_1, self.agent_2]

        while len(possible_actions) > 0:
            current_agent, prev_agent = agents
            game_state = (cards[current_agent], history)

            action = current_agent.choose_action(game_state)
            assert action in KuhnAction.possible_actions(history)

            if action == KuhnAction.BET:
                current_agent.stack_size -= 1
                pot += 1

            agents.reverse()
            history.append(action)
            possible_actions = KuhnAction.possible_actions(history)

        prev_action, action = history[-2:]

        if prev_action == action:
            winner = max(cards, key=cards.get)
        elif prev_action == KuhnAction.BET and action == KuhnAction.PASS:
            winner = prev_agent

        winner.stack_size += pot
        return winner
