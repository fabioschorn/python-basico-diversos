import subprocess
import os

file_path = os.path.join(os.path.dirname(__file__), 'hosts')

def get_ip_addresses(file_path):
    """Read IP addresses from the given file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def add_to_known_hosts(ip_address):
    """Add the SSH key signature of the given IP address to known_hosts."""
    try:
        ssh_keyscan_command = ["ssh-keyscan", ip_address]
        ssh_output = subprocess.check_output(ssh_keyscan_command, stderr=subprocess.STDOUT).decode()

        known_hosts_file = os.path.expanduser("~/.ssh/known_hosts")
        with open(known_hosts_file, "a") as known_hosts:
            known_hosts.write(ssh_output)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing {ip_address}: {e.output.decode()}")

def main():
    hosts_file = 'hosts'
    ip_addresses = get_ip_addresses(hosts_file)

    for ip in ip_addresses:
        print(f"Processing {ip}...")
        add_to_known_hosts(ip)
        print(f"Added {ip} to known_hosts.")

if __name__ == "__main__":
    main()