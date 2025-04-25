from evaluator import *
import os

DESCRIPTION = "This test case checks if the model can generate a script that creates two files: one containing strings and another containing string-palindrome label pairs."

TAGS = ['generate', 'python', 'file-io']

question = '''
Write a Python script that will:
1. Create a list of exactly 100 different strings, of 50 palindromes and 50 non-palindromes. 
   Don't resort to hardcoding strings.
2. Save the strings to a csv file named 'palindrome_data.csv' with two columns:
   - 'text': containing one string per line
   - 'is_palindrome': containing a label that is 1 if the string is a palindrome and 0 if not
   
A string is considered a palindrome if it reads the same forwards and backwards (ignoring case).
For example: "Madam" is a palindrome (label=1), "hello" is not (label=0).

Make sure the script:
- Handles both uppercase and lowercase letters
- Ignores spaces and punctuation when checking for palindromes
- Ensures that no string is repeated
- Uses proper file handling with 'with' statements
- Has clear variable names and comments
- Sets a random seed to ensure reproducibility
- Prints the contents of the csv file as a string to the console and ensure that's the only console output
'''

def check_correctness(csv):
    import pandas as pd
    from io import StringIO
    
    # csv is a string of the csv file contents
    df = pd.read_csv(StringIO(csv))
    
    # Check if the csv file has the correct number of rows
    if len(df) != 100:
        return False, f"The csv file must contain exactly 100 data points. You have {len(df)} data points."
        
    # Check if the csv file has the correct number of palindromes
    if df['is_palindrome'].sum() != 50:
        return False, f"The csv file must contain exactly 50 palindromes and 50 non-palindromes. You have {df['is_palindrome'].sum()} palindromes and {len(df) - df['is_palindrome'].sum()} non-palindromes."
        
    # Check if no string is repeated
    if df['text'].nunique() != 100:
        return False, f"The csv file must contain exactly 100 unique strings. You have {df['text'].nunique()} unique strings."
    
    # Check if the csv file has the correct columns
    if not all(col in df.columns for col in ['text', 'is_palindrome']):
        return False, f"The csv file must contain the columns 'text' and 'is_palindrome'. You have the columns {df.columns}."
    
    for index, row in df.iterrows():
        if row['is_palindrome'] not in [0, 1]:
            return False, f"The is_palindrome column must contain only 0 or 1. You have {row['is_palindrome']} in row {index}."
    
    return True, "The csv file is correct"

def save_csv(csv):
    import pandas as pd
    from io import StringIO
    
    try:
        df = pd.read_csv(StringIO(csv))
        df.to_csv("palindrome_random_data.csv", index=False)
    except Exception as e:
        return False, f"Error saving csv: {e}"
    
    return True, "CSV saved successfully"


TestPalindrome = question >> LLMRun() >> ExtractCode(keep_main=True) >> (Echo() & (PythonRun() >> (Echo() & (PyFunc(check_correctness) >> Echo()) & PyFunc(save_csv))))

if __name__ == "__main__":
    print(run_test(TestPalindrome))
