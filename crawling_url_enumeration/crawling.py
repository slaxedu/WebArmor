import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import yaml
import os

def crawl_urls_for_subdomain(subdomain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/',  # Set the Referer header to a common website
    }

    session = requests.Session()

    try:
        url = f'{subdomain}'  # Assuming subdomains are provided without the protocol
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
    except requests.exceptions.RequestException as e:
        print(f"Error making the request for {subdomain}: {e}")
        return []

def save_all_crawled_urls(all_urls, output_folder):
    filename = os.path.join(output_folder, "crawling_output.txt")
    with open(filename, 'a') as file:  # Use 'a' for append mode
        file.write('\n'.join(all_urls) + '\n')  # Append newlines between subdomains
    print(f"All crawled URLs saved to {filename}")

def main():
    # Load config from config.yaml
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Get output folder path and subdomains file path from config
    output_folder = config["CRAWLING_URL_ENUMERATION"]["OUTPUT_FOLDER_PATH"]
    subdomains_file_path = config["ASSET_DISCOVERY"]["PROBED_SUBDOMAINS_FILE_PATH"]

    # Read probed subdomains from the specified file
    with open(subdomains_file_path, 'r') as file:
        probed_subdomains = [line.strip() for line in file]

    all_crawled_urls = []

    for subdomain in probed_subdomains:
        # Crawl URLs for each probed subdomain
        found_urls = crawl_urls_for_subdomain(subdomain)

        if found_urls:
            all_crawled_urls.extend(found_urls)
            print(f"Crawled URLs for {subdomain}:")
            for url in found_urls:
                print(url)
        else:
            print(f"No URLs found during crawling for {subdomain}.")

    if all_crawled_urls:
        # Save all crawled URLs to a single file
        save_all_crawled_urls(all_crawled_urls, output_folder)
    else:
        print("No URLs found during crawling.")

if __name__ == "__main__":
    main()
