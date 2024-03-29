import yaml
import shodan
import socket
def perform_shodan_operations(config):
    global domain
    domain = config["GLOBAL"]["DOMAIN"]
    shodan_api_key = config["ASSET_DISCOVERY"]["SHODAN_API_KEY"]
    global shodan_file_path
    shodan_file_path = config["ASSET_DISCOVERY"]["SHODAN_FILE_PATH"]

    # Ensure the required parameters are available
    if not domain or not shodan_api_key or not shodan_file_path:
        print("Error: Required parameters not found in the config.")
        return

    # Initialize Shodan API
    api = shodan.Shodan(shodan_api_key)

    # Search for SSL hosts
    try:
        search_results = api.search(f'hostname:{domain} ssl:{domain}', facets={'ip_str': []})
        ipv4_addresses = [result["ip_str"] for result in search_results['matches'] if '.' in result["ip_str"]]
    except shodan.APIError as e:
        print(f"Shodan API error: {e}")
        return

    # Save the IPv4 addresses to the specified file
    with open(shodan_file_path, 'w') as output:
        for ipv4_address in ipv4_addresses:
            output.write(f"{ipv4_address}\n")

    print(f"Done with Shodan operations.")
def get_ip_address(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        with open(shodan_file_path, 'w') as output:
        	output.write(ip_address+'\n')
    except socket.error as e:
        print(f"Error retrieving IP address for {domain_name}: {e}")
        return None
def shodan_operations():
    # Config file path
    config_path = "/root/WebArmor/config.yaml"

    # Load configuration from config.yaml
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    # Run the function
    perform_shodan_operations(config)
    get_ip_address(domain)

# Call the main function if the script is executed directly
if __name__ == "__main__":
    shodan_operations()
