import os
import yaml
import socket
import subprocess
from halo import Halo

def load_configuration():
    config_path = "/root/WebArmor/config.yaml"
    try:
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None



def retrieve_domain_info(domain, output_file):
    try:
        # Get IP address for the domain
        ip_address = socket.gethostbyname(domain)

        # Perform a WHOIS lookup
        whois_output = subprocess.check_output(f"whois {domain}", shell=True, universal_newlines=True)

        # Combine domain information
        output = f"Domain: {domain} => IP Address: {ip_address}\n\nWHOIS Information:\n{whois_output}"

        # Save the output to the specified file
        with open(output_file, 'w') as file:
            file.write(output)

        print("\nDone with Domain Information.\n")
    except Exception as e:
        print(f"Error retrieving domain information: {e}")

def domain_operations():
    spinner = Halo(text="Loading configuration...", spinner="dots")
    spinner.start()

    # Load configuration
    config = load_configuration()
    spinner.stop()

    if config:
        # Retrieve domain information
        domain = config["GLOBAL"]["DOMAIN"]
        output_file = config["ASSET_DISCOVERY"]["DOMAIN_INFO_FILE_PATH"]

        if domain and output_file:
            spinner.start(text="Retrieving domain information...")
            retrieve_domain_info(domain, output_file)
            spinner.stop()
        else:
            print("Error: Domain or domain info file path not found in the config file.")

if __name__ == "__main__":

    # Call the main function with the desired config file path
    domain_operations()
