import subprocess
import sys

def open_redirect_scan(urls_file_path):
    print("\n[-] Scanning for Open_Redirect vulnerability . . .")
    params=['?next', '?url', '?target', '?rurl', '?dest', '?destination', '?redir', '?redirect_uri', '?redirect_url', '?redirect', '/redirect', '/cgi-bin/redirect.cgi', '/out', '/out', '?view', '/login?to', '?image_url', '?go', '?return', '?returnTo', '?return_to', '?checkout_url', '?continue', '?return_path', 'success', 'data', 'qurl', 'login', 'logout', 'ext', 'clickurl', 'goto', 'rit_url', 'forward_url', 'forward', 'pic', 'callback_url', 'jump', 'jump_url', 'click?u', 'originUrl', 'origin', 'Url', 'desturl', 'u', 'page', 'u1', 'action', 'action_url', 'Redirect', 'sp_url', 'service', 'recurl', 'j?url', 'url', 'uri', 'r', 'allinurl', 'q', 'link', 'src', 'tc?src', 'linkAddress', 'location', 'burl', 'request', 'backurl', 'RedirectUrl', 'Redirect', 'ReturnUrl']
    try:
          	with open(urls_file_path,'r') as f:
          		urls=list(set([i.strip() for i in f.readlines() if "=http" in i or '=' in i]))
          	uniq_params=dict()
          	for i in urls:
          		for param in params:
          			if i[:i.index('=')].endswith(param):
          				uniq_params.update({i[:i.index('=')+1]:i[i.index('=')+1:]})
          	clean_urls=[key+value for key,value in uniq_params.items()]
          	if len(clean_urls)==0:
          		print("[!] No Urls that maybe vulnerable for open redirect were found")
          		sys.exit()
          	clean_urlsfile_path='root/WebArmor/owasp_scanning/utils/open_redir_urls.txt'
          	with open(clean_urlsfile_path,'w') as f:
          	             	for i in clean_urls:
          	             		f.write(i+'\n')
    except FileNotFoundError:
          		print("Urls File doesn't exist")
          		sys.exit()	
    try:
        output_file="root/WebArmor/DATA_FOLDER/owasp_scanning/open_redirect.txt"
        command = f"python root/WebArmor/owasp_scanning/utils/opxV3.py -f {clean_urlsfile_path} -o {output_file}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print(f"Output file: {output_file}")
    except Exception as e:
        print(f"Error executing command '{command}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    open_redirect_scan(sys.argv[1])