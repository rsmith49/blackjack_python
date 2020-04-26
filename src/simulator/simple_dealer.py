from .player import BasePlayerHand, PlayerAction


class SimpleDealer(BasePlayerHand):
    """
    A simple dealer that hits soft 17's. It does not split or double down.
    """

    def get_player_state(self):
        """
        For a simple dealer we will only ever see the top cards that are dealt
        """
        return self.hands[0].cards[1:]

    def get_action(self, hand):
        """
        Implements action policy for this simple dealer. If the hand is lower than 17 then hit. If the hand is soft
        17 then hit. If the hand is equal to or above 17 then stay
        """
        if hand.value() < 17 or hand.value() == 17 and hand.is_soft():
            self.perform_action(PlayerAction.HIT)
        else:
            self.perform_action(PlayerAction.STAY)
