# brainfuck gymnasium environment

This repository contains a custom Gymnasium environment designed to simulate a brainfuck interpreter. The environment allows reinforcement learning agents to interact with and learn the Brainfuck programming language.

## Overview

Brainfuck is an esoteric programming language known for its minimalistic design. This environment provides a unique challenge for reinforcement learning agents, as they must learn to interpret and execute brainfuck code efficiently.

All brainfuck instructions are not supported in this environment, not because they cannot be easily implemented, but because they are not necessary for the intended use case. The following instructions are supported:
- `>`: Increment the data pointer
- `<`: Decrement the data pointer
- `+`: Increment the byte at the data pointer
- `-`: Decrement the byte at the data pointer
- `.`: Output the byte at the data pointer
- `NOP`: No operation (used to terminate the program)

## Features

- **Custom Environment**: Built using Gymnasium's custom environment framework.
- **brainfuck Interpreter**: Agents learn to interpret brainfuck code.
- **ASCII Integration**: Utilizes ASCII codes for character manipulation.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Gymnasium library
- NumPy library

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <your-repository-name>
   ```
2. Create a venv:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the custom environment, you can follow the following script. This script demonstrates how to initialize the environment and run a simple agent.

### Testing agent

For testing purposes, I have included a very simple agent that takes a brainfuck code file and runs it.

### Example

```python
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
```

## Resources

- [Gymnasium Custom Environment Documentation](https://gymnasium.farama.org/introduction/create_custom_env)
- [brainfuck Wikipedia Page](https://fr.wikipedia.org/wiki/Brainfuck)
- [ASCII Code Page](https://www.ascii-code.com/)

## Contributing

I have not yet thought about accepting contributions, but I am open to suggestions.

Maybe, when this becomes a bit more mature, I will open it up for contributions. But in the meantime, feel free to fork the repository and make your own changes.
