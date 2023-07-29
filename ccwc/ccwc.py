import argparse
import locale
import sys
import chardet
import os
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
            with open(file_contents, 'r', encoding='utf-8') as file:
                file_data = file.readlines()
                line_count = len(file_data)
        except FileNotFoundError:
            print(f"Error: File not found: {file_contents}")
        except UnicodeDecodeError:
            print(f"Error: Unable to decode the file using 'utf-8' encoding.")
        return line_count


class WordCounter(Counter):
    def count(self, file_contents):
        word_count = 0
        try:
            with open(file_contents, 'r', encoding='utf-8') as file:
                file_data = file.read()
                words = file_data.split()
                word_count = len(words)
        except FileNotFoundError:
            print(f"Error: File not found: {file_contents}")
        except UnicodeDecodeError:
            print(f"Error: Unable to decode the file using 'utf-8' encoding.")
        return word_count


class CharacterCounter(Counter):
    def __init__(self):
        self.preferred_encoding = None

    @staticmethod
    def multibyte_encoding():
        preferred_encoding = locale.getpreferredencoding()
        multibyte_encodings = ['UTF-16', 'UTF-32', 'UTF-8', 'UTF8', 'UTF', 'cp1252']
        return any(encoding.lower() in preferred_encoding.lower() for encoding in multibyte_encodings)

    def count(self, file_contents):
        char_count = 0
        supports_multi_bytes = CharacterCounter.multibyte_encoding()
        if supports_multi_bytes:
            try:
                with open(file_contents, 'rb') as file:
                    file_data = file.read()
                    detected_encoding = chardet.detect(file_data)
                    self.preferred_encoding = detected_encoding['encoding']
                    decoded_content = file_data.decode(self.preferred_encoding)
                    char_count = len(decoded_content)
            except FileNotFoundError:
                print(f"Error: File not found: {file_contents}")
            except UnicodeDecodeError:
                print(f"Error: Unable to decode the file using '{self.preferred_encoding}' encoding.")
        else:
            # If multibyte characters are not supported, fall back to ByteCounter for character count
            byte_counter = ByteCounter()
            char_count = byte_counter.count(file_contents)
        return char_count


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Byte, Line, Word, Character Counter Tool")
        self.parser.add_argument("file_contents", nargs='?', default=None, help="File to process")
        self.shared_args = [
            ("file_contents", {"help": "File to process"}),
            ("-c", {"nargs": '?', "const": "-", "default": None, "help": "Option to count bytes"}),
            ("-l", {"nargs": '?', "const": "-", "default": None, "help": "Option to count lines"}),
            ("-w", {"nargs": '?', "const": "-", "default": None, "help": "Option to count words"}),
            ("-m", {"nargs": '?', "const": "-", "default": None, "help": "Option to count characters"})
        ]
        self.script_path = os.path.abspath(__file__)

        # Add arguments using the shared_args list
        for arg_name, arg_options in self.shared_args:
            self.parser.add_argument(arg_name, **arg_options)

    def parse_args(self):
        args = self.parser.parse_args()
        return args

    def run_single_counter(self, get_counter, cli_option, count_label):
        counter = get_counter()
        total_count = counter.count(cli_option)
        print(f"Number of {count_label}: {total_count} {cli_option}")

    def run(self):
        args = self.parse_args()

        if not sys.stdin.isatty():  # Check if there's input from a pipe (e.g., "cat test.txt | python ccwc.py -c")
            # Read input from standard input (piped content)
            stdin_content = sys.stdin.read()

            if args.c:
                # Count bytes using the ByteCounter and pass stdin_content as the option
                self.run_single_counter(ByteCounter, stdin_content, args.c)
            elif args.l:
                # Count lines using the LineCounter and pass stdin_content as the option
                self.run_single_counter(LineCounter, stdin_content, args.l)
            elif args.w:
                # Count words using the WordCounter and pass stdin_content as the option
                self.run_single_counter(WordCounter, stdin_content, args.w)
            elif args.m:
                # Count characters using the CharacterCounter and pass stdin_content as the option
                self.run_single_counter(CharacterCounter, stdin_content, args.m)
        else:
            # If there's no input from a pipe, handle the script with regular arguments
            if not any([args.c, args.l, args.w, args.m]):
                # If no options are provided, perform all counts
                byte_counter = ByteCounter()
                line_counter = LineCounter()
                word_counter = WordCounter()

                if args.file_contents:
                    # Perform counts on the specified file
                    total_bytes = byte_counter.count(args.file_contents)
                    total_lines = line_counter.count(args.file_contents)
                    total_words = word_counter.count(args.file_contents)
                    print(f"{total_bytes}\t{total_lines}\t{total_words} {args.file_contents}")
                else:
                    # Read from standard input and perform counts
                    for line in sys.stdin:
                        total_bytes = byte_counter.count(line)
                        total_lines = line_counter.count(line)
                        total_words = word_counter.count(line)
                        print(f"{total_bytes}\t{total_lines}\t{total_words} {line}", end="")
            else:
                # Perform individual counts based on the provided options
                if args.c:
                    self.run_single_counter(ByteCounter, args.file_contents, args.c)
                if args.l:
                    self.run_single_counter(LineCounter, args.file_contents, args.l)
                if args.w:
                    self.run_single_counter(WordCounter, args.file_contents, args.w)
                if args.m:
                    self.run_single_counter(CharacterCounter, args.file_contents, args.m)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
