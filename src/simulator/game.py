from typing import List

from .utils import BankruptException
from .player import Player, PlayerHandAgent
from .deck import Deck


class BaseGame:
    """
    Represents a basic game of blackjack with n number of players where each player plays the game based on their
    predefined policy and awards points based on which player(s) win the game. This can be extended to add more
    game features
    """

    def __init__(
            self,
            deck: Deck,
            dealer: PlayerHandAgent,
            *players: List[Player],
            debug=False
    ):
        """
        Initializes the game state. Players are initialized by making the dealer the last player to play

        :param deck: The deck to use for the game
        :param dealer: The PlayerHandAgent object for the dealer
        :param players: Variable number of Player objects that can play
        :param debug: Whether to print debug statements as the game plays
        """
        self.dealer = dealer
        self.deck = deck
        self.players = list(players)

        self.debug = debug

    def reset_hands(self):
        """
        Resets the hands for all the players
        """
        for player in self.players:
            player.reset_hand()

        self.dealer.reset_hand()

    def place_bets(self):
        """
        Places bets for each of the player agents
        """
        for player in self.players:
            # Attempting minor speed boost by only updating the necessary
            # agent at each place
            player.betting_agent.update_model(self)
            player.place_bet()

            if self.debug:
                print(f"Player {player} bets {player.betting_agent.curr_bet}")

    def deal_initial_hands(self):
        """
        This function deals the initial hand for the round to all players
        """
        self._deal_cards()
        self._deal_cards()

    def _deal_cards(self):
        """
        Deals a single card to each player in turn
        """
        for player in self.players:
            player.deal_card(self.deck.next_card())

        self.dealer.deal_card(self.deck.next_card())

    def play_hand(self):
        """
        Plays a round given all the players. Check which players win by comparing their hands
        to the dealer's hand. The dealer is always the last player in this game type
        """
        if self.debug:
            print(f"Dealer showing {self.dealer.hands[0].cards[0]}")
            print("Results:")

        for player in self.players:
            # Attempting minor speed boost by only updating the necessary
            # agent at each place
            player.playing_agent.update_model(self)
            player.play_hand(self.deck)

            if self.debug:
                print(f"  {player}")

        self.dealer.play_hand(self.deck)

        if self.debug:
            print(f"  (Dealer) {self.dealer}")

    def collect_bets(self):
        """
        Pays out or collects money from each player agent
        """
        player_ndxs_to_remove = []

        for player_ndx, player in enumerate(self.players):
            try:
                if self.debug:
                    curr_cash = player.betting_agent.cash

                player.collect_winnings(self.dealer)

                if self.debug:
                    print(f"  Player {player_ndx} wins {player.betting_agent.cash - curr_cash}")

            except BankruptException:
                player_ndxs_to_remove.append(player_ndx)

        # Reversing the list to remove the higher indexes first
        # (so that we don't remove the wrong index from a changing list)
        for ndx in player_ndxs_to_remove[::-1]:
            del self.players[ndx]

    def play_chute(self):
        """
        Plays a round of hands with the chute from start to finish
        """
        # Burn the first card of the chute
        self.deck.next_card()

        while not self.deck.chute_over:
            self.reset_hands()
            self.place_bets()
            self.deal_initial_hands()
            self.play_hand()
            self.collect_bets()
