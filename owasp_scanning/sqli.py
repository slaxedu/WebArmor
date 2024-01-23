import subprocess
import sys
import yaml
from halo import Halo
def scan():
    spinner = Halo(text="Scanning urls for SQL injection . . .", spinner="dots")
    spinner.start()
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    output_folder = config["OWASP"]["SQLI_OUTPUT_PATH"]
    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']

    try:
        with open(urls_file_path, 'r') as f:
            urls = list({i.strip() for i in f.readlines() if "=http" not in i and "=" in i})
        uniq_params = dict()
        
        for i in urls:
            uniq_params.update({i[:i.index('=')+1]: i[i.index('=')+1:]})
        clean_urls = [key + value for key, value in uniq_params.items()]
        clean_urlsfile_path = '/root/WebArmor/owasp_scanning/utils/Sql_URLS.txt'
        with open(clean_urlsfile_path, 'w') as f:
            for i in clean_urls[:10]:
                f.write(i + '\n')
    except FileNotFoundError:
        print("Urls File doesn't exist")
        sys.exit()

    try:
        command = f"sqlmap -m '{clean_urlsfile_path}' --dbs -f --batch --output-dir='{output_folder}' --results-file='/dev/null'"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        #print(f"\nOutput saved to : {output_folder}\n")
        spinner.stop()
    except Exception as e:
        print(f"Error while starting sqlmap: {e}")
        
