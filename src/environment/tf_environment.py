from tensorforce import Environment
from ..simulator.game import BaseGame
from ..simulator.player import PlayerAction
from ..simulator.utils import BlackjackException


class TFBlackjackEnvironment(BaseGame, Environment):
    """
    Class that acts as a tensorforce environment
    """

    def __init__(self, deck, dealer, *players, debug=False):
        super(TFBlackjackEnvironment, self).__init__(deck, dealer, *players, debug=debug)

        self._max_episode_timesteps = 500
        self.sum_multiplier = 0
        self.num_rounds = 0

    def get_stats(self):
        for player in self.players:
            self.sum_multiplier += player.playing_agent.amount_won(self.dealer)
            self.num_rounds += 1

    def print_stats(self):
        print(f"Stats: {self.sum_multiplier/self.num_rounds}")

    def states(self):
        return dict(
            features=dict(type='int', shape=(5,), num_values=23)
        )

    def actions(self):
        return dict(
            type='int', shape=(1,), num_values=4
        )

    def reset(self):
        """
        Resets the game and returns the first observation
        :return: First observation given by self._observe()
        """
        self.deck.shuffle()
        # if self.deck.chute_over:

        self.reset_hands()
        self.place_bets()
        self.deal_initial_hands()

        return self._observe()

    def _observe(self):
        """
        Helper method to return an observation of the current env state
        :return: size 16 array for state specified above
        """
        player_agent = self.players[0].playing_agent
        try:
            player_hand = player_agent.hands[player_agent.curr_hand_ndx]
        except IndexError:
            player_hand = player_agent.hands[player_agent.curr_hand_ndx - 1]

        state = dict(
            features=[
                player_hand.value(),
                self.dealer.hands[0].value(),
                player_hand.is_soft(),
                len(player_hand.cards) == 2,
                len(player_hand.cards) == 2 and (
                        player_hand.cards[0] == player_hand.cards[1]
                )
            ]
        )

        return state

    def execute(self, actions):
        """
        Executes a step of the environment given an action
        """
        # TODO: Obviously this is terrible access practice
        player_hand = self.players[0].playing_agent
        try:
            player_hand._perform_action(
                PlayerAction(actions),
                self.deck
            )
        except ValueError:
            # Probably split or doubled when we couldn't
            return self._observe(), True, -10
        except BlackjackException:
            # if we get a blackjack on first deal calculate reward
            pass

        done = player_hand.curr_hand_ndx >= len(player_hand.hands)

        if done:
            self.dealer.play_hand(self.deck, self)
            self.collect_bets()
            reward = player_hand.amount_won(self.dealer)
        else:
            reward = 0

        obs = self._observe()

        return obs, done, reward


