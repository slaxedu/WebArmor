import subprocess
import yaml

def scan():
    print("\n[~] scanning urls for xxe & ssrf . . .")
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    output_file_path = config["OWASP"]["XXE_SSRF_OUTPUT_PATH"]
    templates_path = config["OWASP"]["TEMPS_PATH"]
    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']

    try:
        with open(urls_file_path, 'r') as f:
            urls = list(set([i.strip() for i in f.readlines()]))
        clean_urls_path = '/root/WebArmor/owasp_scanning/utils/xxe-ssrf-clean-urls.txt'
        with open(clean_urls_path, 'w') as file:
            for i in urls:
                file.write(i+'\n')

        command = f"nuclei -l {clean_urls_path} -t {templates_path} -o {output_file_path}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print(f"Output saved to : {output_file_path}")
    except Exception as e:
        print(f"Error executing command '{command}': {e}")

