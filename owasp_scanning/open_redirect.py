import subprocess
import sys
import yaml
from halo import Halo

def scan():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']
    params = ['?next', '?url', '?target', '?rurl', '?dest', '?destination', '?redir', '?redirect_uri', '?redirect_url', '?redirect', '/redirect', '/cgi-bin/redirect.cgi', '/out', '/out', '?view', '/login?to', '?image_url', '?go', '?return', '?returnTo', '?return_to', '?checkout_url', '?continue', '?return_path', 'success', 'data', 'qurl', 'login', 'logout', 'ext', 'clickurl', 'goto', 'rit_url', 'forward_url', 'forward', 'pic', 'callback_url', 'jump', 'jump_url', 'click?u', 'originUrl', 'origin', 'Url', 'desturl', 'u', 'page', 'u1', 'action', 'action_url', 'Redirect', 'sp_url', 'service', 'recurl', 'j?url', 'url', 'uri', 'r', 'allinurl', 'q', 'link', 'src', 'tc?src', 'linkAddress', 'location', 'burl', 'request', 'backurl', 'RedirectUrl', 'Redirect', 'ReturnUrl']
    
    try:
        with open(urls_file_path, 'r') as f:
            urls = list(set([i.strip() for i in f.readlines() if "=http" in i or '=' in i]))
            uniq_params = {}
            
            for i in urls:
                for param in params:
                    if i[:i.index('=')].endswith(param):
                        uniq_params.update({i[:i.index('=')+1]: i[i.index('=')+1:]})
                        
            clean_urls = [key + value for key, value in uniq_params.items()]
            
            if len(clean_urls) == 0:
                print("[!] No Urls that may be vulnerable for open redirect were found")
                sys.exit()
                
            clean_urlsfile_path = '/sdcard/root/WebArmor/owasp_scanning/utils/open_redir_urls.txt'
            
            with open(clean_urlsfile_path, 'w') as f:
                for i in clean_urls:
                    f.write(i + '\n')
                    
    except FileNotFoundError:
        print("Urls File doesn't exist")
        sys.exit()

    try:
        spinner = Halo(text="Scanning urls for Open_Redirect . . .", spinner="dots")
        spinner.start()
        output_file = config['OWASP']["OP_OUTPUT_PATH"]
        command = f"python /sdcard/root/WebArmor/owasp_scanning/utils/opxV3.py -f {clean_urlsfile_path} -o {output_file}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print(f"\nOutput saved to : {output_file}\n")
        spinner.stop()
        
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
