from .deck import Deck


class BaseGame:
    """
    Represents a basic game of blackjack with n number of players where each player plays the game based on their
    predefined policy and awards points based on which player(s) win the game. This can be extended to add more
    game features
    """

    def __init__(self, initial_deal, dealer, num_decks=6, *players):
        """
        Initializes the game state. Players are initialized by making the dealer the last player to play

        :param initial_deal: The deal object that can deal initial hands to players
        :param dealer: The player object for the dealer
        :param num_decks: The number of decks in this game
        :param players: Variable number of player objects that can play
        """
        self.deck = Deck(num_decks)
        self.initial_deal = initial_deal
        self.players = players + dealer

    def deal_initial_hand(self):
        """
        This function deals the initial hand for the round to all players
        """
        self.initial_deal.deal_initial_hand(self.deck, self.players)

    def play_hand(self):
        """
        Plays a round given all the players. Check which players win by comparing their hands
        to the dealer's hand. The dealer is always the last player in this game type
        """
        for player in self.players:
            player.play_hand(self.deck)

        dealer = self.players[-1:]
        players = self.players[:-1]

        for player in players:
            for hand in player.hands:
                player.winnings += hand.amount_won(dealer.hands[0]) * player.bet


