import os
import requests
import subprocess
import yaml
import re  
from halo import Halo

def download_file(url, folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    response = requests.get(url)

    if response.status_code == 200:
        os.makedirs(folder_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Files downloaded successfully!")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def filter_unique_subdomains(output_folder_path):
    unique_subdomains = set()

    # Iterate over all text files in the output folder
    for filename in os.listdir(output_folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(output_folder_path, filename)
            with open(file_path, 'r') as file:
                # Apply the regex to each line in the file
                for line in file:
                    matches = re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b', line.strip())
                    unique_subdomains.update(matches)

    # Write the unique subdomains to the output file
    output_file_path = os.path.join(output_folder_path, "all-unique-subdomains.txt")
    with open(output_file_path, 'w') as output_file:
        for subdomain in sorted(unique_subdomains):
            output_file.write(f"{subdomain}\n")

    print(f"🧹 Filtering duplicate subdomains...")


def run_command(command, text=""):
    spinner = Halo(text=text, spinner="dots")
    spinner.start()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output = ""
    for line in process.stdout:
        output += line
    process.communicate()
    spinner.stop()
    return output

def subdomains_operations():
    # Load configuration from config.yaml
    config_path = "/root/WebArmor/config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    DOMAIN = config["GLOBAL"]["DOMAIN"]
    OUTPUT_FOLDER_PATH = config["ASSET_DISCOVERY"]["OUTPUT_FOLDER_PATH"]
    SUBDOMAINS_FILE_PATH = config["ASSET_DISCOVERY"]["SUBDOMAINS_FILE_PATH"]
    CHAOS_KEY = config["ASSET_DISCOVERY"]["CHAOS_KEY"]
    NUCLEI_TKO_TEMPLATE = config["ASSET_DISCOVERY"]["NUCLEI_TKO_TEMPLATE"]
    WORDLIST = config["ASSET_DISCOVERY"]["BRUTEFORCE_WORDLIST"]

    # Enumerate subdomains
    print("PASSIVE SUBDOMAINS ENUMERATION")

    print("🔍 Enumerating subdomains using Chaos...")
    run_command(f"chaos -d {DOMAIN} -key {CHAOS_KEY} -silent -o {OUTPUT_FOLDER_PATH}/chaos.txt", text="Chaos")

    print("🔍 Enumerating subdomains using Subfinder...")
    run_command(f"subfinder -d {DOMAIN} -passive -o {OUTPUT_FOLDER_PATH}/subfinder-subs.txt", text="Subfinder")

    # Filtering
    print("🧹 Filtering duplicate subdomains...")
    run_command(f"cat {OUTPUT_FOLDER_PATH}/*.txt | sort -u | tee {OUTPUT_FOLDER_PATH}/all-unique-subdomains.txt", text="Filtering")
    filter_unique_subdomains(OUTPUT_FOLDER_PATH)

    # Checking for Subdomain Takeover using Nuclei
    print("🔎 Checking for subdomain takeover using Nuclei...")
    run_command(f"nuclei -t {NUCLEI_TKO_TEMPLATE} -l {SUBDOMAINS_FILE_PATH} -o {OUTPUT_FOLDER_PATH}/nuclei_tko.txt -c 100", text="Nuclei")

    print(f"✅ All Operations Done. Results saved Successfully!")

if __name__ == "__main__":
    # Call the function
    subdomains_operations()
