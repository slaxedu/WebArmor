import os
import subprocess
import yaml

# Construct the path to the config.yaml file in the parent directory
config_path = os.path.join("..", "config.yaml")

# Load configuration from config.yaml in the parent directory
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

# Get domain from the config
domain = config.get("DOMAIN")
if not domain:
    print("Domain not found in config.yaml. Please add it.")
    exit(1)

# Create a 'data' folder if it doesn't exist
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

def run_osint_task(task_name, enabled_config_key, command, output_filename):
    enabled = config.get(enabled_config_key, True)
    if enabled:
        print(f"Running {task_name}...")
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError:
            print(f"{task_name} command failed")
            exit(1)
        print(f"{task_name} completed. Saving results to {data_folder}/{output_filename}")
        os.rename(output_filename, os.path.join(data_folder, output_filename))
    else:
        print(f"{task_name} skipped in this mode or defined in config.yaml")

# Define OSINT tasks and their associated commands and output filenames
osint_tasks = [
    ("Google Dorks", "GOOGLE_DORKS", f"python3 path/to/dorks_hunter.py -d {domain} -o dorks.txt", "dorks.txt"),
    ("GitHub Dorks", "GITHUB_DORKS", f"python3 path/to/github_dorks.py -d {domain} -o github_dorks.txt", "github_dorks.txt"),
    ("GitHub Repos", "GITHUB_REPOS", f"python3 path/to/github_repos.py -d {domain} -o github_repos.txt", "github_repos.txt"),
    ("Metadata", "METADATA", f"python3 path/to/metadata.py -d {domain} -o metadata_results.txt", "metadata_results.txt"),
    ("Emails", "EMAILS", f"python3 path/to/email_finder.py -d {domain} -o emails.txt", "emails.txt"),
    ("Domain Info", "DOMAIN_INFO", f"python3 path/to/domain_info.py -d {domain} -o domain_info.txt", "domain_info.txt"),
    ("IP Info", "IP_INFO", f"python3 path/to/ip_info.py -d {domain} -o ip_info.txt", "ip_info.txt"),
]

# Run the selected OSINT tasks
for task_name, config_key, command, output_filename in osint_tasks:
    run_osint_task(task_name, config_key, command, output_filename)