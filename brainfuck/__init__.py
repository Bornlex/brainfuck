from enum import Enum
import gymnasium
from gymnasium.core import ObsType, ActType
import numpy as np
from typing import Optional, Any, SupportsFloat

from brainfuck.memory import Memory
from brainfuck.standard_output import StandardOutput
from brainfuck.utils import reward


class Actions(Enum):
    NOP = 0
    INCREMENT_POINTER = 1
    DECREMENT_POINTER = 2
    INCREMENT_VALUE = 3
    DECREMENT_VALUE = 4
    OUTPUT = 5
    INPUT = 6
    START_LOOP = 7
    END_LOOP = 8

    @staticmethod
    def char_to_action(char: str):
        if char == '>':
            return Actions.INCREMENT_POINTER
        elif char == '<':
            return Actions.DECREMENT_POINTER
        elif char == '+':
            return Actions.INCREMENT_VALUE
        elif char == '-':
            return Actions.DECREMENT_VALUE
        elif char == '.':
            return Actions.OUTPUT
        elif char == ',':
            return Actions.INPUT
        elif char == '[':
            return Actions.START_LOOP
        elif char == ']':
            return Actions.END_LOOP
        else:
            return Actions.NOP


class Brainfuck(gymnasium.Env):
    """
    Brainfuck environment.

    Action space is made of the first 5 brainfuck instructions + one NOP indicating the end of the program:
    - 0: NOP
    - 1: >
    - 2: <
    - 3: +
    - 4: -
    - 5: .
    - 6: ,  # unused
    - 7: [  # unused
    - 8: ]  # unused

    The observation space is made of the whole memory + the standard output and the position of the pointer.
    Every character is represented by an integer, its ASCII value.

    In brainfuck specs, the memory is of size 30.000, but we can change it here to simplify the environment.
    """
    def __init__(
            self,
            memory_size: int = 1000,
            standard_output_size: int = 100
    ):
        self.__memory_size = memory_size
        self.__action_size = 5 + 1
        self.__ascii_max_value = 256
        self.__counter_max_value = 1001
        self.__max_signed_value = max(
            self.__ascii_max_value, (self.__counter_max_value - 1) // 2
        )
        self.__standard_output_size = standard_output_size

        self.__max_steps = 100
        self.__max_reward = -(self.__max_steps * reward.INSTRUCTION_PENALTY) * 10

        self.__memory = Memory(size=self.__memory_size)
        self.__standard_output = StandardOutput(max_size=self.__standard_output_size)
        self.__pointer = 0
        self.__current_step = 0

        self.action_space = gymnasium.spaces.Discrete(self.__action_size)
        self.observation_space = gymnasium.spaces.Dict({
            "pointer": gymnasium.spaces.Discrete(self.__memory_size),
            "memory": gymnasium.spaces.MultiDiscrete([
                max(self.__ascii_max_value, self.__counter_max_value)
                for _ in range(self.__memory_size)
            ]),
            "standard_output": gymnasium.spaces.MultiDiscrete([
                self.__ascii_max_value
                for _ in range(self.__standard_output_size)
            ])
        })

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ):
        super().reset(seed=seed)

        self.__pointer = 0
        self.__current_step = 0
        self.__memory.reset()
        self.__standard_output.reset()

        return (
            self.__get_state(),
            self.__get_info()
        )

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """
        Performs an action in the environment and return the next state.

        Because we are in an execution environment, the episode is never over, the agent can always execute one more
        operation. So terminated is always False.
        An episode is over when the agent predicts action 0 (NOP) or when the agent has executed a maximum number of
        steps.
        In the latter, truncated can be True.

        A state is composed of:
        - observation
        - reward
        - terminated (in case the episode is over)
        - truncated (in case the episode is truncated, being too long for example)
        - info (additional information, we do not use it here)
        """
        self.__current_step += 1

        if action == Actions.NOP:
            return (
                self.__get_state(),
                self.__compute_final_reward(),
                True,
                False,
                self.__get_info()
            )
        elif action == Actions.INCREMENT_POINTER:
            self.__increment_pointer()
        elif action == Actions.DECREMENT_POINTER:
            self.__decrement_pointer()
        elif action == Actions.INCREMENT_VALUE:
            self.__increment_value()
        elif action == Actions.DECREMENT_VALUE:
            self.__decrement_value()
        elif action == Actions.OUTPUT:
            self.__output()
        else:
            raise NotImplementedError("Action not implemented")

        return (
            self.__get_state(),
            reward.INSTRUCTION_PENALTY,
            False,
            self.__current_step >= self.__max_steps,
            self.__get_info()
        )

    def render(self, mode: str = "human") -> Optional[Any]:
        """
        Render the environment.
        """
        if mode == 'human':
            print(self.__standard_output.read())

    def __compute_final_reward(self) -> float:
        distance = reward.levenshtein_distance(
            self.__standard_output.read(),
            self.__expected_output
        )

        return min(0, self.__max_reward - distance)

    def __increment_pointer(self):
        if self.__pointer < self.__memory_size - 1:
            self.__pointer += 1

    def __decrement_pointer(self):
        if self.__pointer >= 1:
            self.__pointer -= 1

    def __increment_value(self):
        if self.__memory[self.__pointer] < self.__max_signed_value:
            self.__memory[self.__pointer] += 1

    def __decrement_value(self):
        if self.__memory[self.__pointer] > -self.__max_signed_value:
            self.__memory[self.__pointer] -= 1

    def __output(self):
        value = self.__memory[self.__pointer]
        self.__standard_output.write(value)

    def __get_state(self) -> dict:
        return {
            "pointer": self.__pointer,
            "memory": self.__as_numpy(self.__memory.memory),
            "standard_output": self.__as_numpy(self.__standard_output.raw())
        }

    @staticmethod
    def __as_numpy(array: list[int] | int) -> np.ndarray:
        if isinstance(array, int):
            return np.array([array], dtype=np.int64)

        return np.array(array, dtype=np.int32)

    @staticmethod
    def __get_info() -> dict:
        return {}
