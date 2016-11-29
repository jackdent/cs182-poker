from poker.holdem.agents import InteractiveAgent, RandomAgent
from poker.holdem.game import HoldEmPoker

if __name__ == '__main__':
    BUY_IN = 10
    game = HoldEmPoker(InteractiveAgent(BUY_IN), RandomAgent(BUY_IN))
    game.play()
