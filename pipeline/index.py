import pandas as pd
import re

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('data.csv')

def extract_title(case_text):
    match = re.search(r'\[ G\.R\. No\..*?\]', case_text)
    return match.group(0) if match else 'No Title Found'

df['title'] = df['info'].apply(extract_title)

# Regex pattern that matches the expected title format
pattern = re.compile(r'\[ G\.R\. No\..*?\]')

# Function to check if a title matches the expected format
def is_title_valid(title):
    return bool(pattern.match(title))

# Apply the validation function across all titles
df['is_title_valid'] = df['info'].apply(is_title_valid)

# Count how many titles are invalid
invalid_title_count = (df['is_title_valid'] == False).sum()
print(f"Number of invalid titles: {invalid_title_count}")

# Optional: Inspect some invalid titles to understand the mismatches
print(df[df['is_title_valid'] == False]['info'].sample(10))
