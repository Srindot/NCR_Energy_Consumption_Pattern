import pandas as pd

# 1. Define your file names
excel_file_path = 'your_input_file.xlsx'
csv_file_path = 'your_output_file.csv'

# 2. Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# 3. Convert and save the DataFrame to a CSV file
# The index=False argument is important to avoid writing row numbers into your CSV
df.to_csv(csv_file_path, index=False)

print(f"✅ Successfully converted '{excel_file_path}' to '{csv_file_path}'")