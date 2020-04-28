import os, sys

# Needed for running from the command line with python3 scripts/...
sys.path.append(os.getcwd())

from src.simulator.game import BaseGame
from src.simulator.player import Player
from src.simulator.deck import Deck

from src.agents.betting import ConstantBettingAgent
from src.agents.dealers import SimpleDealer


def main():

    game = BaseGame(
        Deck(),
        SimpleDealer(),
        Player(SimpleDealer(), ConstantBettingAgent(100)),
        Player(SimpleDealer(), ConstantBettingAgent(0)),
        debug=True
    )

    for ndx in range(3):
        print(f"{'-' * 36}Chute {ndx}{'-' * 37}")
        game.deck.shuffle()
        game.play_chute()


if __name__ == '__main__':
    main()
