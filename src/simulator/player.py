"""
Putting the base player behavior here - we can them implement the
player classes in order to create agents that rely on policy
"""
from enum import Enum

from .consts import *
from .utils import BustException, BankruptException, BlackjackException


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

        value = self.value()

        if value > BUST_SCORE:
            raise BustException()
        elif len(self.cards) == 2 and value == BLACKJACK:
            self.blackjack = True

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

    def busted(self):
        """
        Whether the hand busted (went over 21)
        :return: bool
        """
        return self.value() > BUST_SCORE

    def amount_won(self, dealer_hand):
        """
        Returns the multiplier of the original bet that the player
        would get back based on this completed hand vs the dealer
        :param dealer_hand: Score achieved by the dealer
        :return: number between 0 and BLACK_PAYOUT
        """
        # Idk, maybe every speed up counts
        value = self.value()

        if value > BUST_SCORE:  # So we don't have to calculate value again
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


class PlayerHandAgent:
    """
    Base player hand strategy class that should be inherited from to
    enact policy decisions
    NOTE: dealer strategy will also inherit from this
    """
    def __init__(self):
        self.hands = []
        self.curr_hand_ndx = 0

    # Methods to override in inheriting classes

    def update_model(self, game):
        """
        Update the model of the agent from the game state
        :param game: The state of the game
        """
        raise NotImplementedError()

    def get_action(self):
        """
        Driven by the policy of the Player
        :return: PlayerAction enum value
        """
        raise NotImplementedError()

    def get_player_state(self):
        """
        Gets the state of this player. Can be overridden to provide more/less state data
        """
        return self.hands

    # Methods to control game simulation logic - should be no need to override

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

    def play_hand(self, deck, game):
        """
        Performs actions for the hand based on the policy decided by
        self.get_action until the player busts or stays for each hand
        :return:
        """
        while self.curr_hand_ndx < len(self.hands):
            self.update_model(game)
            self._perform_action(self.get_action(), deck)

    def amount_won(self, dealer_hand):
        """
        Gets the multiplier for amount won from the bet for all hands
        :param dealer_hand: PlayerHandAgent of the dealer
        """
        amount_won = 0
        for hand in self.hands:
            amount_won += hand.amount_won(
                # Assuming the dealer only has one hand
                dealer_hand.hands[0]
            )

        return amount_won

    def _perform_action(self, action, deck):
        """
        Performs the action specified by the enum

        NOTE: If needed for args, we can remove this middle man by having the
              self.get_action function just call self.hit etc. directly
        :param action: PlayerAction enum
        :param deck: The deck object to pull cards from
        :return:
        """
        if self.curr_hand_ndx < len(self.hands):
            if action == PlayerAction.STAY:
                self._stay()
            elif action == PlayerAction.HIT:
                self._hit(deck)
            elif action == PlayerAction.SPLIT:
                self._split(deck)
            elif action == PlayerAction.DOUBLE:
                self._double(deck)
        elif self.hands[self.curr_hand_ndx - 1].blackjack:
            raise BlackjackException("You can't perform another since you have a blackjack")
        else:
            raise ValueError("Somehow went passed index without getting blackjack")

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


class PassPlayerHandAgent(PlayerHandAgent):
    """
    Do nothing because we're not using this to train or play the game. Instead we play using
    the environment step function
    """
    def update_model(self, game):
        pass

    def get_action(self):
        pass


# TODO: Maybe make the betting agent able to control amount to double/split
class PlayerBettingAgent:
    """
    Basic player betting agent to inherit from to implement betting strategies
    """
    def __init__(self, buyin, can_lose=False):
        """
        :param buyin: The amount of money the player buys in with
        :param can_lose: If the agent can lose (i.e. go bankrupt)
        """
        self.cash = buyin
        self.can_lose = can_lose
        self.curr_bet = None

    # Methods to override in inheriting classes

    def update_model(self, game):
        """
        Update the model of the agent from the game state
        :param game: The state of the game
        :return:
        """
        raise NotImplementedError()

    def get_bet(self):
        """
        Return the bet to place based on the agent's policy
        :return: A bet amount (float)
        """
        raise NotImplementedError()

    # Methods to control game simulation logic - should be no need to override

    def bet(self):
        """
        Sets the bet amount
        (probably not super needed, but I was thinking for consistnecy of
        just having the agents return an action, and not have to deal with
        setting instance variables or anything)
        """
        self.curr_bet = self.get_bet()

    def collect_winnings(self, multiplier):
        """
        Set the cash to the correct amount based on the bet's outcome
        :param multiplier: A multiplier of the initial bet to add to self.cash
        """
        self.cash += multiplier * self.curr_bet

        if self.can_lose and self.cash < 0:
            raise BankruptException()


class Player:
    """
    A player wrapper that takes a hand strategy and betting agent to perform
    actions as a player
    """
    def __init__(
            self,
            player_hand_agent: PlayerHandAgent,
            betting_agent: PlayerBettingAgent
    ):
        """
        :param player_hand_agent: A PlayerHandAgent that implements policy for
                                  each hand (i.e. hitting, doubling, etc.)
        :param betting_agent: A PlayerBettingAgent that implements betting
                              strategy for each hand
        """
        self.playing_agent = player_hand_agent
        self.betting_agent = betting_agent

    def update_model(self, game):
        """
        Wrapper that updates the "model" of the environment for the agents
        :param game: A Game object containing the state of the game
        """
        # NOTE: Currently unused by the BaseGame
        self.playing_agent.update_model(game)
        self.betting_agent.update_model(game)

    def place_bet(self):
        """
        Wrapper to set the bet for the hand
        """
        self.betting_agent.bet()

    def reset_hand(self):
        """
        Wrapper to reset playing_agent's hand
        """
        self.playing_agent.reset_hand()

    def play_hand(self, deck, game):
        """
        Wrapper to play the hand(s) in the current round
        :param deck:
        """
        self.playing_agent.play_hand(deck, game)

    def deal_card(self, card):
        """
        Wrapper to deal a card to the player hand agent
        :param card: Card to deal
        """
        self.playing_agent.deal_card(card)

    def collect_winnings(self, dealer_hand):
        """
        Updates the cash in self.betting_agent appropriately based on the
        bet and the outcome of the hand
        :param dealer_hand: Hand that the dealer ended up with
        """
        self.betting_agent.collect_winnings(
            self.playing_agent.amount_won(dealer_hand)
        )

    def all_busts(self):
        """
        Returns a boolean of whether all of the player's hands busted
        :return:
        """
        for hand in self.playing_agent.hands:
            if not hand.busted():
                return False

        return True

    def __repr__(self):
        return (
            f"Cash: {self.betting_agent.cash}, " +
            f"Current Hand: {self.playing_agent}"
        )
