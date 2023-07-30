import subprocess

from ccwc import ByteCounter


def test_correct_count_values_with_file():
    # Test correct count values when providing valid file name and option
    with open('test_sample.txt', 'r', encoding='utf-8') as file:
        file_contents = file.read()

    byte_counter = ByteCounter()
    byte_count = byte_counter.count('test_sample.txt')

    assert byte_count == len(file_contents.encode('utf-8'))


def test_standard_input_pipes():
    # Test reading input from standard input using pipes
    pass


def test_input_redirection():
    # Test input redirection to read from a file
    pass


def test_valid_and_invalid_file_names():
    # Test providing valid and invalid file names with different count options
    pass
