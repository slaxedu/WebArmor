import os
import requests
import subprocess
import yaml
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

def subdomains_operations(config_path):
  
    # Load configuration from config.yaml
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    DOMAIN = config["GLOBAL"]["DOMAIN"]
    OUTPUT_FOLDER_PATH = config["ASSET_DISCOVERY"]["OUTPUT_FOLDER_PATH"]
    CHAOS_KEY = config["ASSET_DISCOVERY"]["CHAOS_KEY"]
    NUCLEI_TKO_TEMPLATE = config["ASSET_DISCOVERY"]["NUCLEI_TKO_TEMPLATE"]
    WORDLIST = config["ASSET_DISCOVERY"]["BRUTEFORCE_WORDLIST"]
    RESOLVERS = config["ASSET_DISCOVERY"]["RESOLVERS"]
    
    # Download necessary files
    urls = [
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
        "https://raw.githubusercontent.com/trickest/resolvers/main/resolvers.txt",
        "https://raw.githubusercontent.com/sl4x0/NC-Templates/main/detect-all-takeovers.yaml"
    ]
    utilites_path = config["ASSET_DISCOVERY"]["UTILITIES_FOLDER_PATH"]
    for url in urls:
        filename = url.split("/")[-1]
        if "subdomains" in filename:
            filename = "wordlist.txt"
        elif "resolvers" in filename:
            filename = "resolvers.txt"
        download_file(url, utilites_path, filename)

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

    # Enumerate subdomains
    print("PASSIVE SUBDOMAINS ENUMERATION")
    
    print("🔍 Enumerating subdomains using Chaos...")
    run_command(f"chaos -d {DOMAIN} -key {CHAOS_KEY} -silent -o {OUTPUT_FOLDER_PATH}/chaos.txt", text="Chaos")

    print("🔍 Enumerating subdomains using Amass...")
    run_command(f"amass enum -d {DOMAIN} -passive -o {OUTPUT_FOLDER_PATH}/amass_subs.txt", text="Amass")

    print("🔍 Enumerating subdomains using Subfinder...")
    run_command(f"subfinder -d {DOMAIN} -passive -o {OUTPUT_FOLDER_PATH}/subfinder-subs.txt", text="Subfinder")


    # Active Subdomains Enumeration using PureDNS
    print("ACTIVE SUBDOMAINS ENUMERATION")

    # Active Subdomains Enumeration using Gobuster
    print("🔍 Enumerating subdomains using Gobuster (Bruteforce)...")
    gobuster_output = run_command(f"gobuster dns -w {WORDLIST} -t 50 -o {OUTPUT_FOLDER_PATH}/gobuster_bruteforce_results.txt", text="Gobuster")
    
    # Filtering
    print("🧹 Filtering duplicate subdomains...")
    run_command(f"cat {OUTPUT_FOLDER_PATH}/*.txt | sort -u | tee {OUTPUT_FOLDER_PATH}/all-unique-subdomains.txt", text="Filtering")

    # Checking for Subdomain Takeover using Nuclei
    print("🔎 Checking for subdomain takeover using Nuclei...")
    run_command(f"nuclei -t {NUCLEI_TKO} -l {OUTPUT_FOLDER_PATH}/all-unique-subdomains.txt -o {OUTPUT_FOLDER_PATH}/nuclei_tko.txt -c 100", text="Nuclei")

    print(f"✅ All Operations Done. Results saved Successfully!")

if __name__ == "__main__":
    # Configurability: Allow specifying config file path as a command-line argument
    config_path = "/root/WebArmor/config.yaml"

    # Call the function
    subdomains_operations(config_path)