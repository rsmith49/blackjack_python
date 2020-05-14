from tensorforce import Agent
from src.agents.dealers.simple_dealer import SimpleDealer
from src.agents.betting.simple_betting_agent import ConstantBettingAgent
from src.environment.tf_environment import TFBlackjackEnvironment
from src.simulator.deck import Deck
from src.simulator.player import Player, PassPlayerHandAgent


def main():
    agent_type = 'dqn'
    agent_dir = 'data/dqn'
    model_format = 'tensorflow'
    tensorboard_dir = 'data/summaries'
    tensorboard_labels = ['graph', 'entropy', 'kl-divergence', 'losses', 'rewards']

    environment = TFBlackjackEnvironment(
        Deck(),
        SimpleDealer(),
        Player(PassPlayerHandAgent(), ConstantBettingAgent())
    )

    # try to load agent that exists already, otherwise create a new agent instance
    try:
        agent = Agent.load(
            directory=agent_dir,
            format=model_format,
            environment=environment,
            start_updating=5000,
            memory=10000,
            summarizer=dict(
                directory=tensorboard_dir,
                labels=tensorboard_labels,
                frequency=50,
            )
        )
        print("Loading existing agent for training")
    except ValueError:
        agent = Agent.create(
            agent=agent_type,
            environment=environment,  # alternatively: states, actions, (max_episode_timesteps)
            batch_size=10,
            start_updating=5000,
            memory=10000,
            summarizer=dict(
                directory=tensorboard_dir,
                labels=tensorboard_labels,
                frequency=50,
            )
        )
        print("Creating new agent")

    for ndx in range(100000):
        # Initialize episode
        states = environment.reset()
        terminal = False

        while not terminal:
            # Episode timestep
            actions = agent.act(states=states)
            states, terminal, reward = environment.execute(actions=actions)
            agent.observe(terminal=terminal, reward=reward)

    # save agent after running 300 episodes
    agent.save(directory=agent_dir, append='episodes')

    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
