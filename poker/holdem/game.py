from deuces import Card, Deck, Evaluator
import random

from poker.common import Action, BannerPrinter, Tree

tiny_deck = [135427, 529159,268454953,16787479,67119647,16795671,69634,268446761,139523,16812055]
DECK=tiny_deck

class HoldEmAction(Action):
    ALL = FOLD, CHECK, BET = 'f', 'c', 'b'

    DESCRIPTIONS = {
        FOLD: 'fold',
        CHECK: 'check',
        BET: 'bet'
    }

    VALID_ACTIONS = Tree()
    VALID_ACTIONS[CHECK][CHECK] = True
    VALID_ACTIONS[CHECK][BET][FOLD] = True
    VALID_ACTIONS[CHECK][BET][BET] = True
    VALID_ACTIONS[BET][BET] = True
    VALID_ACTIONS[BET][FOLD] = True


class HoldEmPoker(object):
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, max_hands=1000):
        wins = [0, 0]

        while self.agent_1.stack_size > 0 and self.agent_2.stack_size > 0 and sum(wins) < max_hands:
            agent_order = [self.agent_1, self.agent_2]

            if sum(wins) % 2 == 1:
                agent_order.reverse()

            winner = self.play_hand(agent_order)

            with BannerPrinter():
                if winner:
                    winning_agent = agent_order.index(winner)
                    wins[winning_agent] += 1
                    print('Agent %d won the hand.' % (winning_agent+1))
                else:
                    print('The agents split the pot.')

                print('Agents 1 and 2 now have %d and %d chips, respectively.'
                      % (self.agent_1.stack_size, self.agent_2.stack_size))

        agent_1_win_rate = 100 * wins[0] / sum(wins)
        print('Agent 1 won %d hands, %d%% of the total.' % (wins[0], agent_1_win_rate))
        return wins

    def play_hand(self, agents):
        # Deal cards
        random.shuffle(tiny_deck)
        board = tiny_deck[:5]
        hands = [tiny_deck[5:7], tiny_deck[7:9]]

        winner = None
        history = []
        pot = 0

        # Take blinds
        for agent in agents:
            assert agent.stack_size > 0
            agent.stack_size -= 1
            pot += 1

        current_round = 0
        round_names = ('flop', 'turn', 'river')

        while winner is None and current_round < 3:
            visible_board = board[0:3 + current_round]

            print('At the %s, the board shows:' % round_names[current_round])
            Card.print_pretty_cards(visible_board)

            # If one of the agents is all in, we can end the betting
            if any(agent.stack_size == 0 for agent in agents):
                break

            current_agent = 0
            round_history = []
            possible_actions = HoldEmAction.possible_actions(round_history)

            while winner is None and len(possible_actions) > 0:
                game_state = (visible_board, hands[current_agent], history, round_history)
                action = agents[current_agent].choose_action(game_state, possible_actions)
                assert action in possible_actions

                description = HoldEmAction.DESCRIPTIONS[action]
                print('Agent %d: %s.' % (current_agent + 1, description))

                if action == HoldEmAction.BET:
                    agents[current_agent].stack_size -= 1
                    pot += 1
                elif action == HoldEmAction.FOLD:
                    winner = agents[1 - current_agent]
                else:
                    assert action == HoldEmAction.CHECK

                current_agent = 1 - current_agent
                round_history.append(action)
                possible_actions = HoldEmAction.possible_actions(round_history)

            history.append(round_history)
            current_round += 1

        if winner is None:
            print "CHECKING FOR WINNER"
            # Determine the winner at the showdown
            evaluator = Evaluator()
            scores = [evaluator.evaluate(board, hands[agent]) for agent in range(2)]

            # A smaller score indicates a superior hand
            if scores[0] < scores[1]:
                winner = agents[0]
            elif scores[0] > scores[1]:
                winner = agents[1]
            else:
                agents[0].stack_size += pot / 2
                agents[1].stack_size += pot / 2

                # Returns None if the pot gets split
                return

        winner.stack_size += pot
        return winner
