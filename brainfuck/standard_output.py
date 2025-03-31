class StandardOutput:
    def __init__(self, max_size: int):
        self.__queue = [0] * max_size
        self.__pointer = 0

    def write(self, value: int):
        assert isinstance(value, int), f"Value {value} is not an integer"

        if self.__pointer < len(self.__queue):
            self.__queue[self.__pointer] = value
        else:
            self.__queue[-1] = value

        self.__pointer += 1

    def read(self):
        return ''.join(chr(c) for c in self.__queue)

    def raw(self):
        return self.__queue

    def reset(self):
        self.__queue = [0] * len(self.__queue)
        self.__pointer = 0
