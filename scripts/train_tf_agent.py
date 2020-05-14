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
    tensorboard_dir = f'data/summaries/{agent_type}'
    tensorboard_labels = ['graph', 'entropy', 'kl-divergence', 'losses', 'rewards']
    tensorboard_freq = 50
    start_updating = 5000
    memory = 10000
    batch_size = 10
    num_episodes = 100000

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
            start_updating=start_updating,
            memory=memory,
            summarizer=dict(
                directory=tensorboard_dir,
                labels=tensorboard_labels,
                frequency=tensorboard_freq,
            )
        )
        print("Loading existing agent for training")
    except ValueError:
        agent = Agent.create(
            agent=agent_type,
            environment=environment,
            batch_size=batch_size,
            start_updating=start_updating,
            memory=memory,
            summarizer=dict(
                directory=tensorboard_dir,
                labels=tensorboard_labels,
                frequency=tensorboard_freq,
            )
        )
        print("Creating new agent")

    # Train the agent on the number of episodes specified
    for _ in range(num_episodes):
        states = environment.reset()
        terminal = False

        while not terminal:
            # Episode timestep
            actions = agent.act(states=states)
            states, terminal, reward = environment.execute(actions=actions)
            agent.observe(terminal=terminal, reward=reward)

    # save agent after done training. Attaches num episodes trained on to agent name
    agent.save(directory=agent_dir, append='episodes')

    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
