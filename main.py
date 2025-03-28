import gymnasium

from agents.file_read_agent import FileReadAgent
from brainfuck import Brainfuck


def run_episode(env, agent):
    state = env.reset()
    done = False
    total_reward = 0

    print("=== Rendering environment ===")
    env.render()
    print("=============================")

    while not done:
        action = agent.act(state)
        next_state, reward, done, _, _ = env.step(action)
        state = next_state
        total_reward += reward

    print("=== Rendering environment ===")
    env.render()
    print("=============================")

    return total_reward


if __name__ == '__main__':
    gymnasium.register(
        id='Brainfuck-v0',
        entry_point=Brainfuck,
    )
    e = gymnasium.make('Brainfuck-v0')
    a = FileReadAgent(
        action_space=e.action_space,
        file_path='programs/helloworld_noloop.bf',
    )

    r = run_episode(e, a)
    print(f"Total Reward = {r}")

    e.close()
