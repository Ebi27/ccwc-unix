import subprocess
from ccwc import ByteCounter


def test_correct_count_values_with_file():
    # Test correct count values when providing valid file name and option
    with open('test_sample.txt', 'rb') as file:
        file_contents = file.read()
    # Debugging in Process
    print("file_contents:", repr(file_contents))
    byte_counter = ByteCounter()
    byte_count = byte_counter.count('test_sample.txt')

    assert byte_count == len(file_contents)


def test_input_redirection():
    # Read the contents of the file and strip newline characters
    with open('test_sample.txt', 'r', encoding='utf-8') as file:
        file_contents = file.read().strip()

    # Use input redirection to pass the file contents as input to ccwc.py
    process = subprocess.Popen(['python', 'ccwc.py', '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=file_contents)

    # Print the stdout and stderr for debugging
    print("stdout:", stdout)
    print("stderr:", stderr)

    # Remove carriage return characters from stdout
    stdout = stdout.replace('\r', '')

    # Assert the output matches the expected result (without newline character)
    assert process.returncode == 0
    assert stdout.strip() == "Number of lines: 2"  # Remove the newline character from the assertion


def test_standard_input_pipes():
    # Input data to be passed to ccwc.py through standard input using pipes
    input_data = "The quick brown fox jumps over the lazy dog.\nThis is a test input.\n"

    # Use input redirection to pass the input_data to ccwc.py via standard input
    process = subprocess.Popen(['python', 'ccwc.py', '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=input_data)

    # Debugging in process
    print("stdout:", stdout)
    print("stderr:", stderr)

    # Assert the output matches the expected result
    assert process.returncode == 0
    assert stdout.strip() == "Number of lines: 2"


def test_valid_and_invalid_file_names():
    # Test providing valid and invalid file names with different count options
    pass
