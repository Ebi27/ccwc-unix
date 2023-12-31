# WC-Tool-Coding Challenge #1
This project is a command-line tool that allows you to count the number of words, lines, and bytes in a text file. It provides a simple interface to analyze the content of the file and display the counts accordingly.
It is a solution to the first coding challenge in [John Crickett's Coding Challenge](https://codingchallenges.fyi/challenges/challenge-wc).

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
Make sure you have Docker installed on your system. You can download it from the official Docker website: [https://www.docker.com/get-started](https://www.docker.com/get-started)

### Installation

1. Clone or download this repository to your local machine.


2. Navigate to the project directory:

         cd ccwc/ccwc


3. Install the required dependencies using pip:

         pip install -r chardet

         pip install -U pytest

## Usage

To use the ccwc tool, you can run it from the command-line with the appropriate options.

### Outputs number of bytes
      > docker run -it my_ccwc_image -c test.txt
        341836 test.txt

### Outputs number of Lines
      > docker run -it my_ccwc_image -l test.txt
        7137 test.txt

### Outputs number of Words
      > docker run -it my_ccwc_image -w test.txt
        58159 test.txt

### Outputs number of Characters
      > docker run -it my_ccwc_image -m test.txt
        339120 test.txt

### Default Option (Outputs -c, -l, and -w flags)
      > docker run -it my_ccwc_image test.txt
        7137   58159  341836 test.txt

### Read from standard output
      > cat test.txt | docker run -it my_ccwc_image -l
        7137

## Testing 
This project includes several automated tests to ensure the correctness of the WC tool. 
The tests can be run using `pytest`. To run the tests, make sure you have installed the required 
dependencies (chardet and pytest) as mentioned in the Installation section.

1. Navigate to the project directory (if not already there):
               
         cd ccwc/ccwc

2. Build the docker Image:
   
         docker image build -t my_ccwc_image . 


3. Run the test:
            
         docker run -it my_ccwc_image


The tests will verify the correct count values for valid files, handling of invalid file names, and testing standard input using input redirection and pipes.

**All 6 tests should pass, confirming the tool's functionality and reliability.**


**Note**: The exact command prompt symbols (>, etc.) in the Usage and Testing sections may vary depending on the command-line interface you are using (e.g., Windows Command Prompt, PowerShell, Linux terminal). Adjust them as needed for the appropriate shell.

### Challenge Blogpost 
[Building a wc Unix Tool by Ebi Kpemi-Ogokimi](https://ebixx.hashnode.dev/building-a-wc-unix-tool)


