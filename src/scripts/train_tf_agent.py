from tensorforce import Agent
from src.agents.dealers.simple_dealer import SimpleDealer
from src.agents.betting.simple_betting_agent import ConstantBettingAgent
from src.environment.tf_environment import TFBlackjackEnvironment
from src.simulator.deck import Deck
from src.simulator.player import Player, PassPlayerHandAgent


def main():
    environment = TFBlackjackEnvironment(
        Deck(),
        SimpleDealer(),
        Player(PassPlayerHandAgent(), ConstantBettingAgent())
    )

    # try to load agent that exists already, otherwise create a new agent instance
    try:
        agent = Agent.load(directory='data/vpg', format='tensorflow', environment=environment)
        print("Loading existing agent for training")
    except ValueError:
        print("Creating new agent")
        agent = Agent.create(
            agent='vpg',
            environment=environment,  # alternatively: states, actions, (max_episode_timesteps)
            batch_size=1
        )

    for ndx in range(1000000):
        print()
        # Initialize episode
        states = environment.reset()
        terminal = False

        while not terminal:
            # Episode timestep
            actions = agent.act(states=states)
            states, terminal, reward = environment.execute(actions=actions)
            agent.observe(terminal=terminal, reward=reward)

    # save agent after running 300 episodes
    agent.save(directory='data/vpg', append='episodes')

    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
