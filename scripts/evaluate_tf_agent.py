from tensorforce import Agent
from src.agents.dealers.simple_dealer import SimpleDealer
from src.agents.betting.simple_betting_agent import ConstantBettingAgent
from src.environment.tf_environment import TFBlackjackEnvironment
from src.simulator.deck import CountDeck
from src.simulator.player import Player, PassPlayerHandAgent


def main():
    agent_type = 'dqn'
    agent_dir = f'data/{agent_type}'
    agent_name = 'counting'
    model_format = 'tensorflow'
    num_episodes = 1000000
    debug = False

    environment = TFBlackjackEnvironment(
        CountDeck(),
        SimpleDealer(),
        Player(PassPlayerHandAgent(), ConstantBettingAgent()),
        debug=debug
    )

    agent = Agent.load(
        directory=agent_dir,
        name=agent_name,
        format=model_format,
        environment=environment,
    )

    for _ in range(num_episodes):
        if debug:
            print()

        states = environment.reset()
        terminal = False

        while not terminal:
            actions = agent.act(states=states, evaluation=True)

            if debug:
                print(f"ACTION TAKEN: {actions}")

            states, terminal, _ = environment.execute(actions=actions)
            environment.get_stats()

    environment.print_stats()
    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
