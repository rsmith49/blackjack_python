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
    start_updating = 5000
    memory = 10000
    num_episodes = 500000

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
        start_updating=start_updating,
        memory=memory,
    )

    for _ in range(num_episodes):
        states = environment.reset()
        terminal = False

        while not terminal:
            actions = agent.act(states=states, evaluation=True)
            _, terminal, _ = environment.execute(actions=actions)
            environment.get_stats()

    environment.print_stats()
    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
