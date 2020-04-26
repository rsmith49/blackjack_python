class BaseGame:
    """
    Represents a basic game of blackjack with n number of players where each player plays the game based on their
    predefined policy and awards points based on which player(s) win the game. This can be extended to add more
    game features
    """

    def __init__(self, dealer, deck, *players):
        """
        Initializes the game state. Players are initialized by making the dealer the last player to play

        :param dealer: The player object for the dealer
        :param num_decks: The number of decks in this game
        :param players: Variable number of player objects that can play
        """
        self.dealer = dealer
        self.deck = deck
        self.players = list(players) + [dealer]

    def deal_initial_hand(self):
        """
        This function deals the initial hand for the round to all players
        """
        self.deal_cards()
        self.deal_cards()

    def deal_cards(self):
        """
        Deals a single card to each player in turn
        """
        for player in self.players:
            player.deal_card(self.deck.next_card())

    def reset_hands(self):
        """
        Resets the hands for all the players
        """
        for player in self.players:
            player.reset_hand()

    def play_hand(self):
        """
        Plays a round given all the players. Check which players win by comparing their hands
        to the dealer's hand. The dealer is always the last player in this game type
        """
        for player in self.players:
            player.play_hand(self.deck)

        players = self.players[:-1]

        for player in players:
            for hand in player.hands:
                player.winnings += hand.amount_won(self.dealer.hands[0]) * player.bet


