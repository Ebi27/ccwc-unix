import argparse
import locale
import chardet
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
        self.parser = argparse.ArgumentParser(description="Byte, Line, Word , Character Counter Tool")
        self.parser.add_argument("file_contents", nargs='?', default=None, help="File to process")

        self.parser.add_argument("-c", nargs='?', const="-", default=None, help="Option to count bytes")
        self.parser.add_argument("-l", nargs='?', const="-", default=None, help="Option to count lines")
        self.parser.add_argument("-w", nargs='?', const="-", default=None, help="Option to count words")
        self.parser.add_argument("-m", nargs='?', const="-", default=None, help="Option to count characters")

    def parse_args(self):
        args = self.parser.parse_args()
        return args

    def run(self):
        args = self.parse_args()

        if args.c:
            byte_counter = ByteCounter()
            total_bytes = byte_counter.count(args.c)
            print(f"Number of bytes: {total_bytes} {args.c}")

        elif args.l:
            line_counter = LineCounter()
            total_lines = line_counter.count(args.l)
            print(f"Number of lines: {total_lines} {args.l}")

        elif args.w:
            word_counter = WordCounter()
            total_words = word_counter.count(args.w)
            print(f"Number of words: {total_words} {args.w}")

        elif args.m:
            char_counter = CharacterCounter()
            total_chars = char_counter.count(args.m)
            print(f"Number of characters: {total_chars} {args.m}")

        else:
            # If no options are provided, perform all counts
            byte_counter = ByteCounter()
            line_counter = LineCounter()
            word_counter = WordCounter()

            total_bytes = byte_counter.count(args.file_contents)
            total_lines = line_counter.count(args.file_contents)
            total_words = word_counter.count(args.file_contents)

            print(f"{total_bytes}\t{total_lines}\t{total_words} {args.file_contents}")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
