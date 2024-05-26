import re
from collections import defaultdict
from datetime import datetime

# Define the dictionary for classification
dict_hosts = {
    "cardholder": "1",
    "ecs": "2",
    "ivr": "3",
    "msn": "4",
    "test": "5"
}

def parse_inventory(file_path):
    """
    Parses the given inventory file and organizes the hosts by groups.

    :param file_path: Path to the inventory file.
    :return: Dictionary where keys are group names and values are lists of host entries.
    """
    inventory = defaultdict(list)
    current_group = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            match = re.match(r'\[(.+?)\]', line)
            if match:
                current_group = match.group(1)
            elif current_group:
                inventory[current_group].append(line)
    
    return inventory

def classify_hosts(inventory, dict_hosts):
    """
    Classifies the hosts into new groups based on the hostnames and a provided dictionary.

    :param inventory: Dictionary of hosts organized by their original groups.
    :param dict_hosts: Dictionary containing classification keywords.
    :return: New dictionary with reclassified groups.
    """
    new_inventory = defaultdict(list)
    
    for group, hosts in inventory.items():
        for host in hosts:
            hostname = host.split()[0]
            classified = False
            for key in dict_hosts:
                if key in hostname:
                    new_inventory[f"{group}{key}"].append(host)
                    classified = True
                    break
            if not classified:
                new_inventory[group].append(host)
    
    return new_inventory

def save_inventory(inventory, output_file):
    """
    Saves the classified inventory into a new file.

    :param inventory: Dictionary with reclassified groups and their hosts.
    :param output_file: Path to the output inventory file.
    """
    with open(output_file, 'w') as file:
        for group, hosts in sorted(inventory.items(), key=lambda x: x[0]):
            file.write(f'[{group}]\n')
            for host in hosts:
                file.write(f'{host}\n')
            file.write('\n')

def main(input_file, output_file, dict_hosts):
    """
    Main function that orchestrates the parsing, classification, and saving of the inventory.

    :param input_file: Path to the input inventory file.
    :param output_file: Path to the output inventory file.
    :param dict_hosts: Dictionary containing classification keywords.
    """
    inventory = parse_inventory(input_file)
    classified_inventory = classify_hosts(inventory, dict_hosts)
    save_inventory(classified_inventory, output_file)

if __name__ == "__main__":
    input_file = "/Users/fabioschorn/Documents/VS-Code_FS/python-basico-diversos/examples/ansible-order-by-envs/inventory_all"
    date_str = datetime.now().strftime("%Y_%m_%d")
    output_file = f"/Users/fabioschorn/Documents/VS-Code_FS/python-basico-diversos/examples/ansible-order-by-envs/inventory_groups_{date_str}"
    
    main(input_file, output_file, dict_hosts)