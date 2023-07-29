# WC-Tool-Coding Challenge #1
This project is a command-line tool that allows you to count the number of words, lines, and bytes in a text file. It provides a simple interface to analyze the content of the file and display the counts accordingly.
It is a solution to the first coding challenge in [John Crickett's Coding Challenge](https://codingchallenges.fyi/challenges/challenge-wc).

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

1. Clone or download this repository to your local machine.

2. Navigate to the project directory:
   ```cd wc-tool```

3. Install the required dependencies using pip:
   ```pip install -r chardet```

## Usage

To use the ccwc tool, you can run it from the command-line with the appropriate options.

### Outputs number of bytes
      > ccwc -c test.txt
        341836 test.txt

### Outputs number of Lines
      > ccwc -l test.txt
        7137 test.txt

### Outputs number of Words
      > ccwc -w test.txt
        58159 test.txt

### Outputs number of Words
      > ccwc -m test.txt
        339120 test.txt

### Default Option (Outputs -c, -l, and -w flags)
      > python ccwc test.txt
        7137   58159  341836 test.txt

### Read from standard output
      > cat test.txt | ccwc -l
        7137








