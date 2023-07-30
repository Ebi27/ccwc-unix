import argparse
import locale
import chardet
import sys
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
        self.parser.add_argument("-c", action="store_true", help="Option to count bytes")
        self.parser.add_argument("-l", action="store_true", help="Option to count lines")
        self.parser.add_argument("-w", action="store_true", help="Option to count words")
        self.parser.add_argument("-m", action="store_true", help="Option to count characters")

    def parse_args(self):
        args = self.parser.parse_args()
        return args

    def run(self):
        args = self.parse_args()

        if not sys.stdin.isatty() and not args.file_contents:
            # Read input from standard input (piped content) line by line
            total_lines = 0
            total_bytes = 0
            total_words = 0
            total_chars = 0

            for line in sys.stdin:
                if args.l:
                    total_lines += 1
                if args.c:
                    total_bytes += len(line.encode())
                if args.w:
                    total_words += len(line.split())
                if args.m:
                    total_chars += len(line)

            if args.l:
                print(f"Number of lines: {total_lines}")
            if args.c:
                print(f"Number of bytes: {total_bytes}")
            if args.w:
                print(f"Number of words: {total_words}")
            if args.m:
                print(f"Number of characters: {total_chars}")

        elif args.file_contents:
            # If file_contents is provided, perform counts on the specified file
            if args.l:
                print("File contents:", args.file_contents)  # debugging in process
                line_counter = LineCounter()
                total_lines = line_counter.count(args.file_contents)
                print(f"Number of lines: {total_lines} {args.file_contents}")
            if args.c:
                byte_counter = ByteCounter()
                total_bytes = byte_counter.count(args.file_contents)
                print(f"Number of bytes: {total_bytes} {args.file_contents}")
            if args.w:
                word_counter = WordCounter()
                total_words = word_counter.count(args.file_contents)
                print(f"Number of words: {total_words} {args.file_contents}")
            if args.m:
                char_counter = CharacterCounter()
                total_chars = char_counter.count(args.file_contents)
                print(f"Number of characters: {total_chars} {args.file_contents}")

        elif not any([args.c, args.l, args.w, args.m]) and args.file_contents:
            # If no options are provided, perform all counts
            byte_counter = ByteCounter()
            line_counter = LineCounter()
            word_counter = WordCounter()

            total_bytes = byte_counter.count(args.file_contents)
            total_lines = line_counter.count(args.file_contents)
            total_words = word_counter.count(args.file_contents)

            print(f"{total_bytes}\t{total_lines}\t{total_words} {args.file_contents}")

        else:
            print("Please provide a valid option or filename.")


if __name__ == "__main__":
    cli = CLI()
    cli.run()


