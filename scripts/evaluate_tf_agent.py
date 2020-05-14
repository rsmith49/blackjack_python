from tensorforce import Agent
from src.agents.dealers.simple_dealer import SimpleDealer
from src.agents.betting.simple_betting_agent import ConstantBettingAgent
from src.environment.tf_environment import TFBlackjackEnvironment
from src.simulator.deck import Deck
from src.simulator.player import Player, PassPlayerHandAgent


def main():
    agent_type = 'dqn'
    agent_dir = f'data/{agent_type}'
    model_format = 'tensorflow'

    environment = TFBlackjackEnvironment(
        Deck(),
        SimpleDealer(),
        Player(PassPlayerHandAgent(), ConstantBettingAgent()),
        debug=False
    )

    agent = Agent.load(
        directory=agent_dir,
        format=model_format,
        environment=environment,
        start_updating=5000,
        batch_size=1000,
        memory=10000,
    )

    for _ in range(500000):
        # print()
        # Initialize episode
        states = environment.reset()
        terminal = False

        while not terminal:
            actions = agent.act(states=states, evaluation=True)
            # print(f"Action Taken: {actions}")
            states, terminal, reward = environment.execute(actions=actions)
            # agent.observe(terminal=terminal, reward=reward)
            environment.get_stats()

    environment.print_stats()
    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
