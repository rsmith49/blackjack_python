from src.simulator.player import PlayerBettingAgent


class ConstantBettingAgent(PlayerBettingAgent):
    """
    Simple betting agent that bets a constant amount
    """
    def __init__(self, buyin=50):
        super(ConstantBettingAgent, self).__init__(buyin)

    def get_bet(self):
        return 10

    def update_model(self, game):
        pass


class ZeroBettingAgent(PlayerBettingAgent):
    """
    Simple betting agent that bets ~very~ conservatively
    """
    def __init__(self):
        super(ZeroBettingAgent, self).__init__(0)

    def get_bet(self):
        return 0

    def update_model(self, game):
        pass
