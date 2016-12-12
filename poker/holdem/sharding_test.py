import argparse
import time
from deuces import Card, Deck, Evaluator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='iteration')
    parser.add_argument('-n', help='number_hash_bins')

    i = int(parser.parse_args().i)
    N = int(parser.parse_args().n)

    start_time = time.time()
    for _ in range(100):
        board = None
        while board == None:
            deck = Deck()
            b = deck.draw(5)
            if hash(str(b)) % N == i:
                board = b
    print ("Average time to find a board hash match is %f seconds using %s bins" %((time.time() - start_time)/100., N))
