import argparse
import codecs
from abc import ABC, abstractmethod


class Counter(ABC):
    @abstractmethod
    def count(self, file_contents):
        pass


class ByteCounter(Counter):
    def count(self, file_contents):
        byte_count = 0
        try:
            with open(file_contents, 'rb') as file:
                byte_data = file.read()
                byte_count = len(byte_data)
        except FileNotFoundError:
            print(f"Error: File not found: {file_contents}")
        return byte_count


class LineCounter(Counter):
    def count(self, file_contents):
        line_count = 0
        try:
            with open(file_contents, "r", encoding='utf-8') as file:
                file_data = file.readlines()
                line_count = len(file_data)
        except FileNotFoundError:
            print(f"Error: File not found: {file_contents}")
        except UnicodeDecodeError:
            print(f"Error: Unable to decode the file using 'utf-8' encoding.")
        return line_count


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Byte Counter Tool")
        self.parser.add_argument("-c", nargs='?', const="-", default=None, help="File to count bytes in")
        self.parser.add_argument("-l", nargs='?', const="-", default=None, help="File to count lines in")

    def parse_args(self):
        args = self.parser.parse_args()
        return args

    def run(self):
        args = self.parse_args()
        arg_provided_by_user = any(val is not None for val in vars(args).values())

        if arg_provided_by_user:
            if args.c is not None:
                byte_counter = ByteCounter()
                total_bytes = byte_counter.count(args.c)
                print(f"Number of bytes: {total_bytes}")

        if arg_provided_by_user:
            if args.l is not None:
                line_counter = LineCounter()
                total_lines = line_counter.count(args.l)
                print(f"Number of lines: {total_lines}")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
