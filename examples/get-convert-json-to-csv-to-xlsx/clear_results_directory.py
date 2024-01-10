import os
import json
import pandas as pd
from datetime import datetime

# Clear current working directory
output_directory = 'json_results'

# Get the list of files in the directory and show the list of files
files = os.listdir(output_directory)
print("The following files are in the directory:", files)

# After showing the list of files, remove the files the directory and ignore what is not a json file
for filename in os.listdir(output_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(output_directory, filename)
        os.remove(file_path)

# Show the new status of the directory and the list of files that were removed
files = os.listdir(output_directory)
print("The following files wrere removed from the directory:", files)