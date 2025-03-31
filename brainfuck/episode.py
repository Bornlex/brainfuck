import json
import os


class EpisodeFactory:
    def __init__(self, file_path: str):
        self.__file_path = file_path

        assert self.__file_path.endswith('.jsonl'), 'Episodes file needs to be a jsonl.'
        assert os.path.exists(self.__file_path), f'Episodes file does not exist. Check the path: {self.__file_path}.'

    @property
    def episodes(self):
        with open(self.__file_path) as f:
            line = f.readline()
            while line != "":
                episode = json.loads(line)
                yield episode
                line = f.readline()
