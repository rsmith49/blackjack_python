class Deal:
    """
    Class for declaring the type of dealing methodology
    """

    def deal_initial_hand(self, deck, *players):
        """
        Deals the initial hand to all players in the game
        :param deck: The deck to use to deal hands to each player
        :param players: Variable number of players to deal hands to
        """
        raise NotImplementedError()


class SimpleDeal(Deal):
    """
    Implements a simple "fair" dealing system that buries one card
    and then deals cards one by one to each player in two passes
    """

    def deal_initial_hand(self, deck, *players):
        # bury first card
        deck.next_card()

        # deal two cards to each player, one at a time
        self.deal_card(deck, players)
        self.deal_card(deck, players)

    def deal_card(self, deck, *players):
        """
        Deals a single card to each player in turn
        """
        for player in players:
            player.deal_card(deck.next_card())


