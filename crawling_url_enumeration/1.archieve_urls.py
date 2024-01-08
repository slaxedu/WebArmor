import requests
import json
import yaml
import os

def fetch_archived_urls(subdomain):
    try:
        api_url = f'http://web.archive.org/cdx/search/cdx?url={subdomain}/*&output=json'
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse JSON response and extract URLs
        urls = [entry[2] for entry in json.loads(response.text)]
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching archived URLs for {subdomain}: {e}")
        return []

def save_urls_to_file(urls, output_folder):
    #filename = os.path.join(output_folder, "archived_urls.txt")
    with open(output_folder, 'a') as file:  # Use 'a' mode for append
        file.write('\n'.join(urls) + '\n')  # Append URLs and add a newline
    #print(f"Archived URLs saved to {filename}")

def main():
    # Load config from config.yaml
     #with open('/root/WebArmor/config.yaml', 'r') as config_file:
        #config = yaml.safe_load(config_file)

    # Get output folder path and subdomains file path from config
    output_folder = "mohamed.txt"
    subdomains_file_path = "all_unique_subdomains.txt"

    # Read subdomains from the specified file
    with open(subdomains_file_path, 'r') as file:
        subdomains = [line.strip() for line in file]

    all_archived_urls = []

    # Fetch archived URLs for each subdomain
    for subdomain in subdomains:
        archived_urls = fetch_archived_urls(subdomain)
        all_archived_urls.extend(archived_urls)

    # Save all archived URLs to a single file
    save_urls_to_file(all_archived_urls, output_folder)

if __name__ == "__main__":
    main()
