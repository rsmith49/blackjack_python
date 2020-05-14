from src.simulator.player import PlayerHandAgent, PlayerAction


class BookPlayerAgent(PlayerHandAgent):
    """
    Player agent that plays blackjack according to the book
    """

    hit = PlayerAction.HIT
    stay = PlayerAction.STAY
    double = PlayerAction.DOUBLE
    split = PlayerAction.SPLIT

    """
    "by-the-book" action matrix for hands that are soft and can double
        1  2  3  4  5  6  7  8  9  10
    12  P  P  P  P  P  P  P  P  P  P
    13  H  D  D  H  H  H  H  H  H  H
    14  H  D  D  D  H  H  H  H  H  H
    15  H  D  D  D  H  H  H  H  H  H
    16  H  D  D  D  H  H  H  H  H  H
    17  S  S  S  S  S  S  S  S  S  S
    18  S  S  S  S  S  S  S  S  S  S
    19  S  S  S  S  S  S  S  S  S  S
    20  S  S  S  S  S  S  S  S  S  S
    21  S  S  S  S  S  S  S  S  S  S
    """
    soft_actions_ndx_offset = 12
    soft_actions_double = [
        [split, split, split, split, split, split, split, split, split, split],
        [hit, double, double, hit, hit, hit, hit, hit, hit, hit],
        [hit, double, double, double, hit, hit, hit, hit, hit, hit],
        [hit, double, double, double, hit, hit, hit, hit, hit, hit],
        [hit, double, double, double, hit, hit, hit, hit, hit, hit],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay]
    ]

    """
    by the book action matrix for hands that are soft and can't double
        1  2  3  4  5  6  7  8  9  10
    12  P  P  P  P  P  P  P  P  P  P
    13  H  H  H  H  H  H  H  H  H  H
    14  H  H  H  H  H  H  H  H  H  H
    15  H  H  H  H  H  H  H  H  H  H
    16  H  H  H  H  H  H  H  H  H  H
    17  S  S  S  S  S  S  S  S  S  S
    18  S  S  S  S  S  S  S  S  S  S
    19  S  S  S  S  S  S  S  S  S  S
    20  S  S  S  S  S  S  S  S  S  S
    21  S  S  S  S  S  S  S  S  S  S
    """
    soft_actions = [
        [split, split, split, split, split, split, split, split, split, split],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay]
    ]

    """
    by the book action matrix for hands that aren't soft, can't split, but can double
        1  2  3  4  5  6  7  8  9  10
    4   H  H  H  H  H  H  H  H  H  H    
    5   H  H  H  H  H  H  H  H  H  H
    6   H  H  H  H  H  H  H  H  H  H
    7   H  H  H  H  H  H  H  H  H  H
    8   H  H  H  H  H  H  H  H  H  H
    9   H  D  D  H  H  H  H  H  H  H
    10  H  D  D  D  D  H  H  H  H  H
    11  D  D  D  D  D  D  D  D  D  D
    12  H  S  S  S  S  S  H  H  H  H
    13  H  S  S  S  S  S  H  H  H  H
    14  H  S  S  S  S  S  H  H  H  H
    15  H  S  S  S  S  S  H  H  H  H
    16  H  S  S  S  S  S  H  H  H  H
    17  S  S  S  S  S  S  S  S  S  S
    18  S  S  S  S  S  S  S  S  S  S
    19  S  S  S  S  S  S  S  S  S  S  
    20  S  S  S  S  S  S  S  S  S  S
    21  S  S  S  S  S  S  S  S  S  S
    """
    hard_actions_double_ndx_offset = 4
    hard_actions_double = [
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, double, double, hit, hit, hit, hit, hit, hit, hit],
        [hit, double, double, double, double, hit, hit, hit, hit, hit],
        [double, double, double, double, double, double, double, double, double, double],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay]
    ]

    """
    by the book action matrix for hands that aren't soft, can't split, and can't double
        1  2  3  4  5  6  7  8  9  10
    6   H  H  H  H  H  H  H  H  H  H
    7   H  H  H  H  H  H  H  H  H  H
    8   H  H  H  H  H  H  H  H  H  H
    9   H  H  H  H  H  H  H  H  H  H
    10  H  H  H  H  H  H  H  H  H  H
    11  H  H  H  H  H  H  H  H  H  H
    12  H  S  S  S  S  S  H  H  H  H
    13  H  S  S  S  S  S  H  H  H  H
    14  H  S  S  S  S  S  H  H  H  H
    15  H  S  S  S  S  S  H  H  H  H
    16  H  S  S  S  S  S  H  H  H  H
    17  S  S  S  S  S  S  S  S  S  S
    18  S  S  S  S  S  S  S  S  S  S
    19  S  S  S  S  S  S  S  S  S  S
    20  S  S  S  S  S  S  S  S  S  S
    21  S  S  S  S  S  S  S  S  S  S
    """
    hard_actions_ndx_offset = 6
    hard_actions = [
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [hit, stay, stay, stay, stay, stay, hit, hit, hit, hit],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay]
    ]
    
    
    """
    by the book action matrix for hands that aren't soft but we can split
        1  2  3  4  5  6  7  8  9  10  
    4   H  H  H  H  H  H  H  H  H  H
    6   H  H  H  H  H  H  H  H  H  H
    8   H  H  H  H  H  H  H  H  H  H
    10  H  D  D  D  D  H  H  H  H  H
    12  H  H  H  H  H  H  H  H  H  H
    14  P  P  P  P  P  P  P  P  P  P
    16  P  P  P  P  P  P  P  P  P  P
    18  P  P  P  P  P  P  P  P  P  P
    20  S  S  S  S  S  S  S  S  S  S
    """
    split_action_ndx_offset = 4
    split_action_ndx_multiplier = 2
    split_actions = [
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [hit, double, double, double, double, hit, hit, hit, hit, hit],
        [hit, hit, hit, hit, hit, hit, hit, hit, hit, hit],
        [split, split, split, split, split, split, split, split, split, split],
        [split, split, split, split, split, split, split, split, split, split],
        [split, split, split, split, split, split, split, split, split, split],
        [stay, stay, stay, stay, stay, stay, stay, stay, stay, stay]
    ]

    def __init__(self):
        super().__init__()

        self.dealer_card = 0

    def update_model(self, game):
        self.dealer_card = game.dealer.hands[0].cards[1]

    def get_action(self):
        """
        Uses the game state to get the action that this player should perform.
        This player plays "by the book"
        """
        dealer_hand_ndx = self.dealer_card - 1
        curr_hand = self.hands[self.curr_hand_ndx]
        is_soft = curr_hand.is_soft()
        can_split = curr_hand.can_split()
        can_double = curr_hand.can_double()

        if is_soft:
            hand_ndx = curr_hand.value() - BookPlayerAgent.soft_actions_ndx_offset
            if can_double:
                return BookPlayerAgent.soft_actions_double[hand_ndx][dealer_hand_ndx]
            else:
                return BookPlayerAgent.soft_actions[hand_ndx][dealer_hand_ndx]
        else:
            if can_split:
                hand_ndx = int((curr_hand.value() - BookPlayerAgent.split_action_ndx_offset) / BookPlayerAgent.split_action_ndx_multiplier)
                return BookPlayerAgent.split_actions[hand_ndx][dealer_hand_ndx]
            elif can_double:
                hand_ndx = curr_hand.value() - BookPlayerAgent.hard_actions_double_ndx_offset
                return BookPlayerAgent.hard_actions_double[hand_ndx][dealer_hand_ndx]
            else:
                hand_ndx = curr_hand.value() - BookPlayerAgent.hard_actions_ndx_offset
                return BookPlayerAgent.hard_actions[hand_ndx][dealer_hand_ndx]



