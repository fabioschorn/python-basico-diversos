import subprocess
import os

file_path = os.path.join(os.path.dirname(__file__), 'hosts')

def get_ip_addresses(file_path):
    """Read IP addresses from the given file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def is_ip_in_known_hosts(ip_address, known_hosts_file):
    """Check if the IP address is already in the known_hosts file."""
    try:
        with open(known_hosts_file, 'r') as file:
            for line in file:
                if ip_address in line:
                    return True
        return False
    except FileNotFoundError:
        # If the file doesn't exist, treat it as if the IP is not in it.
        return False

def add_to_known_hosts(ip_address):
    """Add the SSH key signature of the given IP address to known_hosts."""
    known_hosts_file = os.path.expanduser("~/.ssh/known_hosts")

    if is_ip_in_known_hosts(ip_address, known_hosts_file):
        print(f"{ip_address} is already in known_hosts.")
        return

    try:
        ssh_keyscan_command = ["ssh-keyscan", ip_address]
        ssh_output = subprocess.check_output(ssh_keyscan_command, stderr=subprocess.STDOUT).decode()

        with open(known_hosts_file, "a") as known_hosts:
            known_hosts.write(ssh_output)
        print(f"Added {ip_address} to known_hosts.")

    except subprocess.CalledProcessError as e:
        print(f"Error adding {ip_address} to known_hosts.")
        print(f"SSH Error Output: {e.returncode}")

def main():
    ip_addresses = get_ip_addresses(file_path)

    for ip in ip_addresses:
        print(f"Processing {ip}...")
        add_to_known_hosts(ip)

if __name__ == "__main__":
    main()