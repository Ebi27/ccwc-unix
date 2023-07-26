from abc import ABC, abstractmethod


class Counter(ABC):
    @abstractmethod
    def count(self, file_contents):
        pass


class CLI:
    def parse_args(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    cli = CLI()
    cli.run()
