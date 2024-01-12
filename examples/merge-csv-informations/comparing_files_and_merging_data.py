import pandas as pd

# Read the CSV files
csv_file_1 = '/YOUR-PATH/report_aws_agents_failure.csv'  # Update the path to your first CSV file
csv_file_2 = '/YOUR-PATH/account_instance_name_ip.csv'  # Update the path to your second CSV file

df1 = pd.read_csv(csv_file_1)
df2 = pd.read_csv(csv_file_2)

# Create a mapping from name to ip in the second DataFrame
name_to_ip_map = dict(zip(df2['name'], df2['ip']))

# Map the ip to the first DataFrame, default to 'pending ip' if not found
df1['ip'] = df1['instanceName'].map(name_to_ip_map).fillna('pending ip')

# Save the enriched DataFrame to a new CSV file
output_csv = '/YOUR-PATH/enriched_csv.csv'  # You can change the name of the output file
df1.to_csv(output_csv, index=False)

print(f"New CSV file created: {output_csv}")