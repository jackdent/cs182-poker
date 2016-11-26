from deuces import Card, Deck, Evaluator


class BannerPrinter(object):
    def __init__(self, token='=', repeat=40):
        self.token = token
        self.repeat = repeat

    def __enter__(self):
        print(self.token * self.repeat)

    def __exit__(self, *exc):
        print(self.token * self.repeat)


class Action(object):
    FOLD, CHECK, CALL, BET = range(4)


class Agent(object):
    def __init__(self, stack_size):
        self.stack_size = stack_size

    def choose_action(self):
        raise NotImplementedError


class InvalidActionError(Exception):
    def __init__(self, agent, action):
        self.agent = agent
        self.action = action


class InteractiveAgent(Agent):
    def choose_action(self, board, hand, pot):
        while True:
            print('Your hand is:')
            Card.print_pretty_cards(hand)

            print('You have %d chips remaining.' % self.stack_size)

            action = raw_input('Enter "f" to fold, "ch" to check, "ca" to call or "b" to bet: ' )

            if action == 'f':
                return Action.FOLD
            elif action == 'ch':
                return Action.CHECK
            elif action == 'ca':
                return Action.CALL
            elif action == 'b':
                return Action.BET
            else:
                print('Unknown action "%s", please try again.' % action)


class HoldEmPoker(object):
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, max_hands=1000):
        hand = 0

        while self.agent_1.stack_size > 0 and self.agent_2.stack_size > 0 and hand < max_hands:
            agents = [self.agent_1, self.agent_2]
            if hand % 2 == 1:
                agents.reverse()

            winner = self.play_hand(agents)

            with BannerPrinter():
                if winner:
                    print('Agent %d won the hand.' % 1 if winner is self.agent_1 else 2)
                else:
                    print('The agents split the pot.')

                print('Agents 1 and 2 now have %d and %d chips, respectively.'
                      % (self.agent_1.stack_size, self.agent_2.stack_size))

            hand += 1

    def play_hand(self, agents):
        pot = 0
        winner = None

        # Take blinds
        for agent in agents:
            assert agent.stack_size > 0
            agent.stack_size -= 1
            pot += 1

        # Deal cards
        deck = Deck()
        hands = [deck.draw(2), deck.draw(2)]
        board = deck.draw(5)

        for r in range(3, 5):
            visible_board = board[0:r]

            print('The board shows:')
            Card.print_pretty_cards(visible_board)

            # If one of the agents is all in, we can end the betting
            if agents[0].stack_size == 0 or agents[1].stack_size == 0:
                break

            # Round 1: first player can either check or bet
            first_action = agents[0].choose_action(visible_board, hands[0], pot)

            if first_action == Action.BET:
                agents[0].stack_size -= 1
                pot += 1
            else:
                if first_action != Action.CHECK: raise InvalidActionError(agents[0], first_action)

            # Round 2: if first player checked, second player
            # can either check or bet. If first player bet,
            # second player can either fold or call.
            second_action = agents[1].choose_action(visible_board, hands[1], pot)

            if second_action == Action.FOLD:
                if first_action != Action.BET: raise InvalidActionError(agents[1], second_action)
                winner = agents[0]
                break
            elif second_action == Action.CHECK:
                if first_action != Action.CHECK: raise InvalidActionError(agents[1], second_action)
            elif second_action == Action.CALL:
                if first_action != Action.BET: raise InvalidActionError(agents[1], second_action)
                agents[1].stack_size -= 1
                pot += 1
            elif second_action == Action.BET:
                if first_action != Action.CHECK: raise InvalidActionError(agents[1], second_action)
                agents[1].stack_size -= 1
                pot += 1

            # Round 3: if second player bet, first player has
            # the option to either fold or call.
            if second_action == Action.BET:
                assert first_action == Action.CHECK
                third_action = agents[0].choose_action(visible_board, hands[0], pot)

                if third_action == Action.FOLD:
                    winner = agents[1]
                    break
                elif third_action == Action.CALL:
                    agents[0].stack_size -= 1
                    pot += 1
                else:
                    raise InvalidActionError(agents[0], third_action)

        if winner is None:
            # Determine the winner at the showdown
            evaluator = Evaluator()
            scores = [evaluator.evaluate(board, hands[0]),
                      evaluator.evaluate(board, hands[1])]

            # A smaller score indicates a superior hand
            if scores[0] < scores[1]:
                winner = agents[0]
            elif scores[0] > scores[1]:
                winner = agents[1]
            else:
                agents[0].stack_size += pot / 2
                agents[1].stack_size += pot / 2

                # Returns None if there pot gets split
                return

        winner.stack_size += pot
        return winner


if __name__ == '__main__':
    BUY_IN = 10
    game = HoldEmPoker(InteractiveAgent(BUY_IN), InteractiveAgent(BUY_IN))
    game.play()

