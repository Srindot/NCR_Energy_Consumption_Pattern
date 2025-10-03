# Use this simple script on your newly cleaned file
import pandas as pd

# Make sure this points to your new, cleaned file
df = pd.read_excel('Data/EST_Project_5min_Dataset.xlsx')

df.to_csv('Data/data.csv', index=False)

print("✅ Conversion successful!")