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
    tensorboard_freq = 20
    memory = 10000
    batch_size = 20
    num_episodes = 10000000
    learning_rate = 3e-7
    exploration = 0.2
    summarizer = dict(
        directory=tensorboard_dir,
        labels=tensorboard_labels,
        frequency=tensorboard_freq,
    )
    should_load = False
    debug = False

    environment = TFBlackjackEnvironment(
        Deck(),
        SimpleDealer(),
        Player(PassPlayerHandAgent(), ConstantBettingAgent()),
        debug=debug
    )

    if should_load:
        agent = Agent.load(
            directory=agent_dir,
            format=model_format,
            environment=environment,
            memory=memory,
            learning_rate=learning_rate,
            exploration=exploration,
            summarizer=summarizer
        )
        print("Loading existing agent for training")
    else:
        agent = Agent.create(
            agent=agent_type,
            environment=environment,
            batch_size=batch_size,
            memory=memory,
            exploration=exploration,
            summarizer=summarizer
        )
        print("Creating new agent")

    # Train the agent on the number of episodes specified
    for _ in range(num_episodes):
        if debug:
            print()

        states = environment.reset()
        terminal = False

        while not terminal:
            # Episode timestep
            actions = agent.act(states=states)

            if debug:
                print(f"ACTION TAKEN: {actions}")

            states, terminal, reward = environment.execute(actions=actions)
            agent.observe(terminal=terminal, reward=reward)

    # save agent after done training. Attaches num episodes trained on to agent name
    agent.save(directory=agent_dir, append='episodes')

    agent.close()
    environment.close()


if __name__ == '__main__':
    main()
