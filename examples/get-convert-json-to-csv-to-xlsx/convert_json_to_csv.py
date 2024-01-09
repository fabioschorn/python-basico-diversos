import pandas as pd

# Read the JSON file
df = pd.read_json (r'./data.json')
# Convert to CSV
df.to_csv (r'./data.csv', index = None)