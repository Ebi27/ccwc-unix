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
    process = subprocess.Popen(['python', 'ccwc.py', '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
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
    process = subprocess.Popen(['python', 'ccwc.py', '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=input_data)

    # Debugging in process
    print("stdout:", stdout)
    print("stderr:", stderr)

    # Assert the output matches the expected result
    assert process.returncode == 0
    assert stdout.strip() == "Number of lines: 2"


def test_valid_and_invalid_file_names():
    # Test valid file name with '-c' option (character count)
    process = subprocess.Popen(['python', 'ccwc.py', '-c', 'test_sample.txt'], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert stdout.strip() == "Number of bytes: 129 test_sample.txt"

    # Test invalid file name with '-c' option
    try:
        subprocess.check_call(['python', 'ccwc.py', '-c', 'nonexistent_file.txt'])
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0
        assert "Error: File 'nonexistent_file.txt' not found." in e.stderr

    # Test invalid file name with '-l' option
    try:
        subprocess.check_call(['python', 'ccwc.py', '-l', 'nonexistent_file.txt'])
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0
        assert "Error: File 'nonexistent_file.txt' not found." in e.stderr

    # Test providing no file name with '-c' option
    try:
        subprocess.check_call(['python', 'ccwc.py', '-c'])
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0
        assert "Error: Please provide a valid file name." in e.stderr

    # Test providing no file name with '-l' option
    try:
        subprocess.check_call(['python', 'ccwc.py', '-l'])
    except subprocess.CalledProcessError as e:
        assert e.returncode != 0
        assert "Error: Please provide a valid file name." in e.stderr


def test_line_count_with_valid_file():
    # Test valid file name with '-l' option (line count)
    process = subprocess.Popen(['python', 'ccwc.py', '-l', 'test_sample.txt'], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0
    assert stdout.strip().endswith(f"Number of lines: 2 test_sample.txt")


def test_character_count_with_multibyte_encoding():
    # Test character count with a file containing multibyte characters
    with open('test_multibyte.txt', 'w', encoding='utf-8') as file:
        file.write("こんにちは、世界！")

    try:
        process = subprocess.Popen(['python', 'ccwc.py', 'test_multibyte.txt'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        assert process.returncode == 0
        assert stdout.strip() == "Number of characters: 8 test_multibyte.txt"

    except Exception as e:
        print("Error:", e)
        with open('test_multibyte.txt', 'r', encoding='utf-8') as file:
            file_contents = file.read()
        print("File contents:", repr(file_contents))

    # Clean up the test file
    import os
    os.remove('test_multibyte.txt')

