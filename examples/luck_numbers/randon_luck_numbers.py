import random
import csv

def read_base_numbers_from_csv(file_path):
    base_numbers = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            base_numbers.append([int(num) for num in row])
    return base_numbers

def generate_combination():
    combination = []
    while len(combination) < 6:
        num = random.randint(1, 60)
        if num not in combination:
            combination.append(num)
    return sorted(combination)

def is_close_to_base(new_combination, base_numbers):
    for base in base_numbers:
        close_count = 0
        for num in new_combination:
            if num in range(min(base)-2, max(base)+3):
                close_count += 1
        if close_count >= 1:
            return True
    return False

# Assuming the CSV file is in the same location as the Python script
csv_file_path = 'base_numbers.csv'

# Read base numbers from the CSV file
base_numbers = read_base_numbers_from_csv(csv_file_path)

# Generate a new combination that is close to the base numbers
new_combination = generate_combination()
while not is_close_to_base(new_combination, base_numbers):
    new_combination = generate_combination()

new_combination = sorted(new_combination)
print(new_combination)