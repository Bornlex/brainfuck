

class Memory:
    def __init__(self, size: int = 30000):
        self.__size = size
        self.__memory = [0] * self.__size

    def __getitem__(self, key: int) -> int:
        assert 0 <= key < self.__size, f"Index {key} out of bounds"

        return self.__memory[key]

    def __setitem__(self, key: int, value: int) -> None:
        assert 0 <= key < self.__size, f"Index {key} out of bounds"
        assert isinstance(value, int), f"Value {value} is not an integer"

        self.__memory[key] = value

    @property
    def memory(self) -> list[int]:
        return self.__memory

    def reset(self):
        self.__memory = [0] * self.__size
