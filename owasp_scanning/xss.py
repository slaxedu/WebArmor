import subprocess
import yaml
from halo import Halo

def scan():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']

    with open(urls_file_path, 'r') as f:
        urls = list({i.strip() for i in f.readlines() if "=" in i and "redir=" not in i and "r=" not in i})

    uniq_params = {}
    for i in urls:
        uniq_params.update({i[:i.index('=') + 1]: i[i.index('=') + 1:]})
    clean_urls = [key + value for key, value in uniq_params.items()]

    clean_urls_path = '/sdcard/root/WebArmor/owasp_scanning/utils/cleanXss.txt'

    with open(clean_urls_path, 'w') as f:
        for i in clean_urls:
            f.write(i + '\n')

    try:
        spinner = Halo(text="Scanning urls for xss . . .", spinner="dots")
        spinner.start()
        for xurl in clean_urls[:2]:
            try:
                out = config['OWASP']["XSS_OUTPUT_PATH"]
                command = f"~/go/bin/./dalfox url '{xurl}' --only-poc='r,v'  -o '{out}'"

                process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.wait()
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
        print(f"\nOutput saved to: {out}\n")
        spinner.stop()

    except Exception as e:
        print(f"An error occurred: {e}")
