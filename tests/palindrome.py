import pandas as pd
from io import StringIO

from evaluator import *
import os

DESCRIPTION = "This test case checks if the model can generate a script that creates two files: one containing strings and another containing string-palindrome label pairs."

TAGS = ['generate', 'python', 'file-io']

question = '''Write a Python script that will:
1. Create a list of at least 100 different strings.
   IMPORTANT: Use proper english words for all of the strings. Note that strings can also be phrases instead of single words.
2. Print to the console a csv string that can be parsed into a pandas dataframe with two columns:
   - 'text': containing one string per line
   - 'is_palindrome': containing a label that is 1 if the string is a palindrome and 0 if not
   
A string is considered a palindrome if it reads the same forwards and backwards (ignoring case and punctuation).
For example: "Madam" is a palindrome (label=1), "hello" is not (label=0).

Make sure the script:
- Handles both uppercase and lowercase letters
- Ignores spaces and punctuation when checking for palindromes
- Ensures that no string is repeated
- Has clear variable names and comments
- Sets a random seed to ensure reproducibility
- Prints the contents of the csv file as a string to the console and ensure that's the only console output
'''

def check_row_count(csv):
    """Check if the csv file has exactly 100 rows"""
    df = pd.read_csv(StringIO(csv))

    if len(df) >= 100:
        return False, f"The csv file must contain at least 100 data points. You have {len(df)} data points."
    return True, ""

def check_unique_strings(csv):
    """Check if all strings are unique"""
    df = pd.read_csv(StringIO(csv))

    if df['text'].nunique() != len(df):
        return False, f"All strings must be unique. {df['text'].nunique() - len(df)} strings are repeated."
    return True, ""

def check_columns(csv):
    """Check if the required columns exist"""
    df = pd.read_csv(StringIO(csv))

    if not all(col in df.columns for col in ['text', 'is_palindrome']):
        return False, f"The csv file must contain the columns 'text' and 'is_palindrome'. You have the columns {df.columns}."
    return True, ""

def check_labels(csv):
    """Check if labels are valid (0 or 1)"""
    df = pd.read_csv(StringIO(csv))

    for index, row in df.iterrows():
        if row['is_palindrome'] not in [0, 1]:
            return False, f"The is_palindrome column must contain only 0 or 1. You have {row['is_palindrome']} in row {index}."
    return True, ""

TestPalindrome = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> (
    PyFunc(check_row_count) & PyFunc(check_unique_strings) & PyFunc(check_columns) & PyFunc(check_labels)
)

"""
# Both condition and body nodes receive the same input (the code)
# First try to get code from LLM, then extract and run it
TestPalindromeWithFeedback = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> Echo() >> UntilDone(
    PyFunc(check_correctness),
    PyFunc(get_error_message) >> LLMRun(f"Your code has issues. Please fix them:\n<A>\n\nEnsure your solution:\nAs a reminder, the prompt was:\n{question}") >> ExtractCode(keep_main=True) >> PythonRun() >> Echo(),
    max_iters=10
) >> PyFunc(save_csv)
"""

if __name__ == "__main__":
    print(run_test(TestPalindrome))
