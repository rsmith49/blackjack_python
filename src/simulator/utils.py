class BustException(Exception):
    """
    Signals a player has busted (gone over 21)
    """


class BankruptException(Exception):
    """
    Signals that a player has gone bankrupt and must leave the table (Game)
    """


class BlackjackException(Exception):
    """
    Signals when a player gets dealt a blackjack
    """
