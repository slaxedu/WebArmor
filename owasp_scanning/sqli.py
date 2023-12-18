import subprocess
import sys

def sqli_scan(urls_file_path):
    print("\n[~] Scanning for SQL injection . . .")
    
    try:
    	with open(urls_file_path,'r') as f:
    		urls=list(set([i.strip() for i in f.readlines() if "=http" not in i and "=" in i]))
    	uniq_params=dict()
    	for i in urls:
    		uniq_params.update({i[:i.index('=')+1]:i[i.index('=')+1:]})
    	clean_urls=[key+value for key,value in uniq_params.items()]
    	clean_urlsfile_path='root/WebArmor/owasp_scanning/utils/Sql_URLS.txt'
    	with open(clean_urlsfile_path,'w') as f:
    		for i in clean_urls:
    			f.write(i+'\n')
    except FileNotFoundError:
    	print("Urls File doesn't exist")
    	sys.exit()	
    try:
        command = f"sqlmap -m '{clean_urlsfile_path}' --dbs -f --batch --output-dir='root/WebArmor/DATA_FOLDER/owasp_scanning/' --results-file='/dev/null'"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print("Output saved to: root/WebArmor/DATA_FOLDER/owasp_scanning/")
    except Exception as e:
        print(f"Error while starting sqlmap: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    sqli_scan(sys.argv[1])
  