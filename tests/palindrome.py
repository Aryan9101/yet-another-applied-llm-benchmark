import pandas as pd
from io import StringIO

from evaluator import *
import os

DESCRIPTION = "This test case checks if the model can generate a script that creates a CSV file containing strings with labels indicating whether each string is a palindrome."

TAGS = ['generate', 'python', 'file-io', 'palindrome']

question = '''Write a Python script that will:
1. Create a list of at least 100 different strings.
   IMPORTANT: Use proper English words for all of the strings. Note that strings can also be phrases instead of single words.
2. Print to the console a csv string that can be parsed into a pandas dataframe with two columns:
   - 'string': the word or phrase
   - 'is_palindrome': a boolean value (True/False) or integer (1/0) indicating if the string is a palindrome

A palindrome reads the same backward as forward, ignoring spaces, punctuation, and case.
Examples: "racecar" is a palindrome, "A man, a plan, a canal: Panama" is a palindrome, "hello" is not a palindrome.

Make sure the script:
- Ensures that no string is repeated
- Has clear variable names and comments
- Sets a random seed to ensure reproducibility
- Prints the contents of the csv file as a string to the console and ensure that's the only console output
- Includes a good mix of both palindromes and non-palindromes
'''

def check_row_count(csv):
    """Check if the csv file has exactly 100 rows"""
    df = pd.read_csv(StringIO(csv))

    if len(df) < 100:
        return False, f"The csv file must contain at least 100 data points. You have {len(df)} data points."
    return True, ""

def check_unique_strings(csv):
    """Check if all strings are unique"""
    df = pd.read_csv(StringIO(csv))

    if df['string'].nunique() != len(df):
        return False, f"All strings must be unique. {len(df) - df['string'].nunique()} strings are repeated."
    return True, ""

def check_columns(csv):
    """Check if the required columns exist"""
    df = pd.read_csv(StringIO(csv))

    if not all(col in df.columns for col in ['string', 'is_palindrome']):
        return False, f"The csv file must contain the columns 'string' and 'is_palindrome'. You have the columns {df.columns}."
    return True, ""

TestPalindrome = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> (
    PyFunc(check_row_count) & PyFunc(check_unique_strings) & PyFunc(check_columns)
)

if __name__ == "__main__":
    print(run_test(TestPalindrome))
