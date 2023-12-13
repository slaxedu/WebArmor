import os
import yaml
import httpx
from halo import Halo

def probe_subdomains(subdomains, output_file):
    spinner = Halo(text="Probing Webservers", spinner="dots")
    spinner.start()

    probed_subdomains = []

    # Probe subdomains for both HTTP and HTTPS
    for subdomain in subdomains:
        url_http = f"http://{subdomain}"
        url_https = f"https://{subdomain}"
        
        try:
            # Try HTTP
            response_http = httpx.head(url_http)
            if response_http.status_code in (200, 301, 302):
                probed_subdomains.append(url_http)
            
            # Try HTTPS
            response_https = httpx.head(url_https)
            if response_https.status_code in (200, 301, 302):
                probed_subdomains.append(url_https)
        
        except httpx.RequestError:
            pass  # Ignore connection errors

    spinner.stop()

    # Save the probing results
    with open(output_file, 'w') as file:
        for subdomain in probed_subdomains:
            file.write(f"{subdomain}\n")

    return probed_subdomains

def subs_probing():
    # Load configuration from config.yaml
    config_path = "/root/WebArmor/config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    
    SUBDOMAINS_FILE_PATH = config["SUBDOMAINS_FILE_PATH"]
    OUTPUT_FOLDER_PATH = config["OUTPUT_FOLDER_PATH"]

    # Read subdomains from the specified file
    with open(SUBDOMAINS_FILE_PATH, 'r') as file:
        subdomains = [line.strip() for line in file.readlines()]

    # Probing Subdomains
    output_file = os.path.join(OUTPUT_FOLDER_PATH, "probed_subs.txt")
    probed_subs = probe_subdomains(subdomains, output_file)

    print(f"✅ Subdomain probing done.")

# Call the main function if the script is executed directly
if __name__ == "__main__":
    subs_probing()
