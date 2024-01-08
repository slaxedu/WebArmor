import subprocess
import yaml
import sys

def scan():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']
    print("[~] Scanning urls for xss . . .")
    
    with open(urls_file_path, 'r') as f:
        urls = list(set([i.strip() for i in f.readlines() if "=" in i and "redir=" not in i and "r=" not in i]))
        
    uniq_params = dict()
    for i in urls:
        uniq_params.update({i[:i.index('=') + 1]: i[i.index('=') + 1:]})
    clean_urls = [key + value for key, value in uniq_params.items()]
    
    clean_urls_path = '/root/WebArmor/owasp_scanning/utils/xss_urls.txt'
    
    with open(clean_urls_path, 'w') as f:
        for i in clean_urls:
            f.write(i+'\n')

    try:
        for xurl in clean_urls:
            try:
                out = config['OWASP']["XSS_OUTPUT_PATH"]
                command = f"dalfox url '{xurl}' --only-poc='r,v' -o '{out}'"
                
                process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.wait()
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
        print(f"Output saved to: {out}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    scan()
    print(f"Output saved to: {out}")
