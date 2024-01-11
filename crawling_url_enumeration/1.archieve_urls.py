import requests
import json
import yaml
import os

def fetch_archived_urls(domain):
    try:
        api_url = f'http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json'
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse JSON response and extract URLs
        urls = [entry[2] for entry in json.loads(response.text)]
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching archived URLs for {domain}: {e}")
        return []

def save_urls_to_file(urls, output_folder):
    filename = os.path.join(output_folder, "archived_urls.txt")
    with open(filename, 'a') as file:  # Use 'a' mode for append
        file.write('\n'.join(urls) + '\n')  # Append URLs and add a newline
    print(f"Archived URLs for {domain} saved to {filename}")

def main():
    # Load config from config.yaml
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Get domain and output folder path from config
    domain = config["DOMAIN"]
    output_folder = config["CRAWLING_URL_ENUMERATION"]["OUTPUT_FOLDER_PATH"]

    # Fetch archived URLs for the specified domain
    archived_urls = fetch_archived_urls(domain)

    if archived_urls:
        # Save all archived URLs to a single file
        save_urls_to_file(archived_urls, output_folder)
        print(f"All archived URLs for {domain} saved to a single file.")
    else:
        print(f"No archived URLs found for {domain}.")

if __name__ == "__main__":
    main()
