import subprocess
import sys
import yaml

def xss_scan(urls_file):
    print("[~] Scanning urls for xss . . .")
    with open(urls_file, 'r') as urls:
        xss_urls = [i.strip() for i in urls.readlines() if "=" in i]
    xss_urls_path = 'root/WebArmor/owasp_scanning/utils/xss_urls.txt'
    with open(xss_urls_path, 'w') as f:
        for i in xss_urls:
            f.write(i)

    try:
        with open(xss_urls_path, 'r') as o:
            vuln_urls = [i for i in o.readlines()]
    except FileNotFoundError:
        print("No xss urls file was found ! ")

    for xurl in vuln_urls:
        try:
            with open('/root/WebArmor/config.yaml', 'r') as config_file:
                config = yaml.safe_load(config_file)
            output_file = config["OWASP"]["XSS_OUTPUT_PATH"]
            command = f"dalfox url '{xurl}' -o '{output_file}' --waf-evasion --deep-domxss --mining-dict --mining-dom"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
        except Exception as e:
            print(f"Error executing command '{command}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    input_file = sys.argv[1]
    xss_scan(input_file)
    print("Output saved to: root/WebArmor/DATA_FOLDER/owasp_scanning/xss.txt")
