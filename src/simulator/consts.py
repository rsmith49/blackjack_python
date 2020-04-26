BLACKJACK = 21  # Blackjack
BUST_SCORE = 21  # Idk, maybe they could be different
ACE = 1
ACE_BONUS = 10  # Optional additional score an Ace can give

BLACKJACK_PAYOUT = 1.5  # Multiplier from bet to add to funds

# Max score where you can still use the ACE_BONUS without busting
SOFT_SCORE_CUTOFF = BUST_SCORE - ACE_BONUS
