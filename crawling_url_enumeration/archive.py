import requests
import json
import yaml
from halo import Halo

def archived_urls_collector(domain):
    if target not in domain:
        return []
    try:
        api_url = f'http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json'
        response = requests.get(api_url)
        response.raise_for_status()
        urls = [entry[2] for entry in json.loads(response.text)]
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching or saving archived URLs for {domain}: {e}")
        return []

def fetch_archived_urls():
    all_urls = []
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    output_folder = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']
    domains_path = config['ASSET_DISCOVERY']['SUBDOMAINS_FILE_PATH']
    global target
    target = config['GLOBAL']['DOMAIN']
    with open(domains_path, 'r') as f:
        domains = [i.strip() for i in f.readlines()]
    spinner = Halo(text="Fetching URLs from web archive . . .", spinner="dots")
    spinner.start()
    for i in domains:
        all_urls.extend(archived_urls_collector(i))
    with open(output_folder, 'w') as f:
        for url in all_urls:
            f.write(url + '\n')
    print(f"\nAll archived URLs were saved to: {output_folder}\n")
    spinner.stop()
