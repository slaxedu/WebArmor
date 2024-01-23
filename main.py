import os
from datetime import datetime
import sys
import yaml
from asset_discovery import (domain_operations, subdomains_operations, subs_probing, subs_technolgoies, shodan_operations)
from crawling_url_enumeration import (archive, crawler)
from network_scanning import Network_scanner
from owasp_scanning import (xss, open_redirect, sqli, xxe_ssrf)
from vulnerability_scanning import vulnerability_scanner
from reporting import (INFO_reporter, URLS_reporter, NETWORK_reporter, OWASP_reporter, VULNSCAN_reporter)

# ANSI escape codes for text color
GREEN = "\033[32m"
RED = "\033[91m"
RESET = "\033[0m"
PURPLE = "\033[95m"
BOLD = "\033[1m"

# Function to print colored text
def print_colored(name, value, color):
    print(f"{BOLD}{name}{RESET} : {BOLD}{color}{value}{RESET}\n")

# Print scan date and time
current_datetime = datetime.now()
scan_date = current_datetime.strftime("%d %B %Y")
scan_time = current_datetime.strftime("%H:%M:%S")

config_file_path = "/root/WebArmor/config.yaml"
existence_message = "FOUND" if os.path.exists(config_file_path) else "NOT FOUND"
existence_color = GREEN if os.path.exists(config_file_path) else RED

def delete_text_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") and file != "all_urls.txt":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

delete_text_files('DATA_FOLDER/')

msg = """
░██╗░░░░░░░██╗███████╗██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝
░░████╔═████║░██╔══╝░░██╔══██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░

░█████╗░██████╗░███╗░░░███╗░█████╗░██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗██╔══██╗
███████║██████╔╝██╔████╔██║██║░░██║██████╔╝
██╔══██║██╔══██╗██║╚██╔╝██║██║░░██║██╔══██╗
██║░░██║██║░░██║██║░╚═╝░██║╚█████╔╝██║░░██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚═╝"""
print(msg + '\n')

print_colored("Scan date", scan_date, GREEN)
print_colored("Scan start time", scan_time, GREEN)
print_colored("Config file default path", config_file_path, existence_color)
print_colored("Config file state", existence_message, existence_color)

if not os.path.exists(config_file_path):
    print(f"{BOLD}{RED}[ERROR] config file doesn't exist{RESET}")
    sys.exit(1)

try:
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    target = config['GLOBAL']['DOMAIN']
    subs_path = config['ASSET_DISCOVERY']['SUBDOMAINS_FILE_PATH']
except Exception as e:
    print(f"{BOLD}{RED}[ERROR] YAML config may not be valid{RESET}")
    sys.exit(1)

print_colored("Target", target, PURPLE)

start = datetime.now()

try:
    domain_operations.domain_operations()
    subdomains_operations.subdomains_operations()
    try:
        with open(subs_path, 'r') as f:
            subs_count = len([i for i in f.readlines()])
            print_colored("No. of subdomains", subs_count, GREEN)
    except (FileExistsError, FileNotFoundError):
        subs_count = "Subdomains file wasn't found"
        print_colored("No. of subdomains", subs_count, RED)
        sys.exit(1)

    subs_probing.subs_probing()
    subs_technolgoies.subs_technologies()
    shodan_operations.shodan_operations()

    #archive.fetch_archived_urls()
    #crawler.crawl_urls()
    print(f"\nAll archived URLs were saved\n")
    print(f"\nAll crawled URLs were saved\n")

    Network_scanner.launch_scan()

    vulnerability_scanner.launch_scan()
    vulnerability_scanner.start_fuzzing()

    xss.scan()
    open_redirect.scan()
    sqli.scan()
    xxe_ssrf.scan()

    URLS_reporter.generate_html_report()
    NETWORK_reporter.generate_html_report()
    OWASP_reporter.generate_html_report()
    VULNSCAN_reporter.generate_html_report()
    INFO_reporter.generate_html_report()

    print(f"{BOLD}{GREEN}WEB-ARMOR SCANNING DONE SUCCESSFULLY ✓{RESET}")
    print_colored("Duration", f'{datetime.now()-start}', GREEN)

except Exception as e:
    print_colored("An error occurred", " current scan aborted", RED)
    sys.exit(1)
