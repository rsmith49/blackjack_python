"""
Putting the base player behavior here - we can them implement the
player classes in order to create agents that rely on policy
"""
from enum import Enum

from .consts import *


class BustException(Exception):
    """
    Signals a player has busted (gone over 21)
    """


class Hand:
    """
    Deals with the calculation of the value of a player's hand
    """
    def __init__(self, *cards):
        """
        :param cards: Variable number of card values to start the hand with
        """
        self.cards = list(cards)
        self.doubled = False

        # If we got blackjack on the constructor, then it's blackjack
        if self.value() == BLACKJACK:
            self.blackjack = True
        else:
            self.blackjack = False

    def add_card(self, card_val, double=False):
        """
        Adds the card to this hand
        :param card_val: integer representing the card value
        :param double: Flag to indicate the card was added via a double
        :return:
        """
        self.cards.append(card_val)

        if double:
            self.doubled = True

        if self.value() > BUST_SCORE:
            raise BustException()

    def value(self):
        """
        Returns the value of the hand
        :return:
        """
        hand_value = sum(self.cards)
        for card in self.cards:
            # If we can make any of the Aces worth 11, do it
            if card == ACE and hand_value <= SOFT_SCORE_CUTOFF:
                hand_value += ACE_BONUS

        return hand_value

    def is_soft(self):
        """
        Whether the hand is a "soft" hand
        (i.e. it contains an Ace that is acting as an 11)
        :return: bool
        """
        return sum(self.cards) != self.value()

    def amount_won(self, dealer_hand):
        """
        Returns the multiplier of the original bet that the player
        would get back based on this completed hand vs the dealer
        :param dealer_hand: Score achieved by the dealer
        :return: number between 0 and BLACK_PAYOUT
        """
        # Idk, maybe every speed up counts
        value = self.value()

        if value > BUST_SCORE:
            amount = -1

        elif self.blackjack:
            amount = BLACKJACK_PAYOUT

        elif dealer_hand.value() > BUST_SCORE or value > dealer_hand.value():
            amount = 1

        elif value == dealer_hand.value():
            # Push
            amount = 0

        else:
            amount = -1

        if self.doubled:
            amount *= 2

        return amount

    def __repr__(self):
        return str(self.cards)


class PlayerAction(Enum):
    STAY = 0
    HIT = 1
    SPLIT = 2
    DOUBLE = 3


class BasePlayerHand:
    """
    Base player hand class to inherit from to enact policy decisions
    NOTE: dealer will also inherit from this
    """

    def __init__(self):
        self.hands = []
        self.curr_hand_ndx = 0
        self.bet = 0
        self.winnings = 0

    def reset_hand(self):
        """
        Resets the player's hand
        """
        self.hands = []
        self.curr_hand_ndx = 0

    def deal_card(self, card):
        """
        Deals a card to this player. Card is added to current hand. Creates a hand if the player doesn't
        already have one
        :param card: The card dealt to this player.
        """
        if not self.hands:
            self.hands.append(Hand(card))
        else:
            hand = self.hands[self.curr_hand_ndx]
            hand.add_card(card)

    def play_hand(self, deck):
        """
        Performs actions for the hand based on the policy decided by
        self.get_action until the player busts or stays for each hand
        :return:
        """
        while self.curr_hand_ndx < len(self.hands):
            self.perform_action(self.get_action(), deck)

    def get_player_state(self):
        """
        Gets the state of this player. Can be overridden to provide more/less state data
        """
        return self.hands

    def get_action(self):
        """
        Driven by the policy of the Player
        :return: PlayerAction enum value
        """
        raise NotImplementedError()

    def update_state(self, game):
        """
        Update the state of the agent with the game state
        :param game: The state of the game
        """
        raise NotImplementedError()

    def perform_action(self, action, deck):
        """
        Performs the action specified by the enum

        NOTE: If needed for args, we can remove this middle man by having the
              self.get_action function just call self.hit etc. directly
        :param action: PlayerAction enum
        :param deck: The deck object to pull cards from
        :return:
        """
        if action == PlayerAction.STAY:
            self._stay()
        elif action == PlayerAction.HIT:
            self._hit(deck)
        elif action == PlayerAction.SPLIT:
            self._split(deck)
        elif action == PlayerAction.DOUBLE:
            self._double(deck)

    def _stay(self):
        self.curr_hand_ndx += 1

    def _hit(self, deck):
        try:
            self.hands[self.curr_hand_ndx].add_card(
                deck.next_card()
            )
        except BustException:
            self.curr_hand_ndx += 1

    def _double(self, deck):

        if len(self.hands[self.curr_hand_ndx].cards) > 2:
            raise ValueError("Can't double after the initial deal")

        try:
            self.hands[self.curr_hand_ndx].add_card(
                deck.next_card(),
                double=True
            )
        except BustException:
            # Doubled, so we're done with the hand regardless
            pass

        self.curr_hand_ndx += 1

    def _split(self, deck):
        old_hand = self.hands[self.curr_hand_ndx]
        # Figured we may as well throw this validation here
        if len(old_hand.cards) != 2 or old_hand.cards[0] != old_hand.cards[1]:
            raise ValueError("Can't split on non-matching hand")

        self.hands[self.curr_hand_ndx] = Hand(
            old_hand.cards[0],
            deck.next_card()
        )
        self.hands.insert(
            self.curr_hand_ndx + 1,
            Hand(
                old_hand.cards[1],
                deck.next_card()
            )
        )

    def __repr__(self):
        output = ""

        for hand in self.hands:
            output += f"VALUE: {hand.value()}, CARDS: {hand}"

        return output
