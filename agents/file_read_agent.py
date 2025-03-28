from brainfuck import Actions


class FileReadAgent:
    def __init__(self, action_space, file_path: str):
        self.__action_space = action_space
        self.__file_path = file_path
        self.__content = self.__read_file()
        self.__pointer = 0

    def act(self, observation):
        if self.__pointer < len(self.__content):
            char = self.__content[self.__pointer]
            self.__pointer += 1

            return Actions.char_to_action(char)

        return Actions.char_to_action('NOP')

    def reset(self):
        self.__pointer = 0

    def __read_file(self):
        with open(self.__file_path, 'r') as file:
            return file.read()
