from Wappalyzer import Wappalyzer, WebPage
import yaml
from halo import Halo
from requests.exceptions import SSLError
import sys

def detect_technologies(config):
    wappalyzer = Wappalyzer.latest()

    results = {}
    probed_subdomains_file_path = config["ASSET_DISCOVERY"]["PROBED_SUBDOMAINS_FILE_PATH"]
    technologies_file_path = config["ASSET_DISCOVERY"]["TECHNOLOGIES_FILE_PATH"]

    if not probed_subdomains_file_path or not technologies_file_path:
        print("Error: Paths not found in the config.")
        return

    try:
        with open(probed_subdomains_file_path, 'r') as file:
            subdomains = [line.strip() for line in file.readlines()]

        with open(technologies_file_path, 'w') as output:
            with Halo(text="Detecting technologies", spinner="dots"):
                for subdomain in subdomains:
                    try:
                        webpage = WebPage.new_from_url(subdomain)
                        technologies = wappalyzer.analyze(webpage)
                        results[subdomain] = technologies
                        output.write(f"{subdomain} => {technologies}\n")
                    except SSLError as ssl_error:
                        # Suppress SSL errors
                        pass
                    except Exception as e:
                        print(f"Error analyzing {subdomain}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    return results

def subs_technologies():
    # Config file path
    config_path = "/root/WebArmor/config.yaml"

    # Load configuration from config.yaml
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    # Run the function and save the results
    subdomains_with_technologies = detect_technologies(config)

    # Print a message indicating the completion of the script
    print("Done with detecting technologies.\n")

# Call the main function if the script is executed directly
if __name__ == "__main__":
    subs_technologies()
