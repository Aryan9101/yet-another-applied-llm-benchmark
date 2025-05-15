import pandas as pd
from io import StringIO

from evaluator import *
import os

DESCRIPTION = "This test case checks if the model can generate a script that creates two files: one containing strings and another containing string-palindrome label pairs."

TAGS = ['generate', 'python', 'file-io']

question = '''Write a Python script that will:
1. Create a list of at least 100 different strings.
   IMPORTANT: Use random strings of random lengths.
2. Print to the console a csv string that can be parsed into a pandas dataframe with two columns:
   - 'question': a question asking how many times a letter appears in a word
   - 'answer': the number of times the letter appears in the word

For example: "How many times does the letter 'a' appear in the word 'xjalsfss'?" should have an answer of 3.

Make sure the script:
- Ensures that no word is repeated
- Has clear variable names and comments
- Sets a random seed to ensure reproducibility
- Prints the contents of the csv file as a string to the console and ensure that's the only console output
'''

def check_row_count(csv):
    """Check if the csv file has exactly 100 rows"""
    df = pd.read_csv(StringIO(csv))

    if len(df) < 100:
        return False, f"The csv file must contain at least 100 data points. You have {len(df)} data points."
    return True, ""

def check_unique_questions(csv):
    """Check if all questions are unique"""
    df = pd.read_csv(StringIO(csv))

    if df['question'].nunique() != len(df):
        return False, f"All questions must be unique. {df['question'].nunique() - len(df)} questions are repeated."
    return True, ""

def check_columns(csv):
    """Check if the required columns exist"""
    df = pd.read_csv(StringIO(csv))

    if not all(col in df.columns for col in ['question', 'answer']):
        return False, f"The csv file must contain the columns 'question' and 'answer'. You have the columns {df.columns}."
    return True, ""

def check_answers(csv):
    """Check if answers are valid integers"""
    df = pd.read_csv(StringIO(csv))

    for index, row in df.iterrows():
        if not isinstance(row['answer'], int):
            return False, f"The answer column must contain only integers. You have {row['answer']} in row {index}."
    return True, ""

TestStrawberryRandom = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> (
    PyFunc(check_row_count) & PyFunc(check_unique_questions) & PyFunc(check_columns) & PyFunc(check_answers)
)

if __name__ == "__main__":
    print(run_test(TestStrawberryRandom))
