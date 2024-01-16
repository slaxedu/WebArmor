import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import yaml
from halo import Halo

def crawl(domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/',
    }

    session = requests.Session()

    try:
        url = f'http://{domain}'
        response = session.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tags = soup.find_all('a')

        urls = []
        for tag in anchor_tags:
            href = tag.get('href')
            if href:
                absolute_url = urljoin(url, href)
                urls.append(absolute_url)

        return urls
    except requests.exceptions.RequestException:
        return []


def crawl_urls():
    all_urls = []
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    output_folder = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']
    domains_path = config['ASSET_DISCOVERY']['SUBDOMAINS_FILE_PATH']
    with open(domains_path, 'r') as f:
        domains = [i.strip() for i in f.readlines()]
    spinner = Halo(text="Crawling URLs . . .", spinner="dots")
    spinner.start()
    for i in domains:
        all_urls.extend(crawl(i))
    with open(output_folder, 'a') as f:
        for url in all_urls:
            f.write(url + '\n')
    print(f"\nAll crawled URLs were saved to: {output_folder}\n")
    spinner.stop()
