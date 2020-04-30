import numpy as np

# Values for blackjack cards from Ace through King for each suit
CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
CARDS_IN_DECK = 52


class Deck:
    """
    Simulates a dealer's deck(s)
    """
    def __init__(self, num_decks=6, reshuffle_perc=0.8, random_seed=None):
        """
        :param num_decks: Number of decks the dealer uses to shuffle
        :param reshuffle_perc: The proportion through all cards where the
                               decks are re-shuffled
        :param random_seed: A random seed to initialize the random number
                            generator, so we can repeat experiments
        """
        self.num_decks = num_decks
        self.reshuffle_at = int(reshuffle_perc * num_decks * CARDS_IN_DECK)

        if random_seed is not None:
            np.random.seed(random_seed)

        # Put these here so PyCharm would stop yelling at me
        self.cards = None
        self.card_index = 0
        self.chute_over = False

        self.shuffle()

    def shuffle(self):
        """
        Shuffles the cards and resets the current card index
        :return:
        """
        self.card_index = 0
        self.cards = CARD_VALUES * self.num_decks

        np.random.shuffle(self.cards)
        self.chute_over = False

    def next_card(self):
        """
        Returns the next card in the deck
        :return: Value of card returned
        :raises: EndOfChuteException
        """
        card = self.cards[self.card_index]
        self.card_index += 1

        if self.card_index >= self.reshuffle_at:
            self.chute_over = True

        return card

    def cards_dealt(self):
        """
        Get the cards that have already been dealt at this point
        :return: list of card values
        """
        return self.cards[:self.card_index]

    def cards_shown(self):
        """
        Slight variation of `self.cards_dealt` that only returns cards
        that have been shown (the dealer "burns" the first card in a chute)
        :return:
        """
        return self.cards[1:self.card_index]

    def cards_left(self):
        """
        Get the cards left in the deck at this point
        :return: list of card values
        """
        return self.cards[self.card_index + 1:]
