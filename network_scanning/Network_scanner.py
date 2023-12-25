import nmap
import yaml

def scan():
    print("[-] Scanning target's network . . .")
    nm = nmap.PortScanner()
    output_content = ""
    
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    ip_file_path = config['ASSET_DISCOVERY']['SHODAN_FILE_PATH']

    try:
        with open(ip_file_path, 'r') as file:
            ip_list = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{ip_file_path}' not found.")
        return

    for ip in ip_list:
        try:
            nm.scan(ip, arguments='--top 300 -sV')
            if ip not in nm.all_hosts():
                raise KeyError
            state = nm[ip].state()
        except (nmap.PortScannerError, KeyError):
            state = 'down'

        result = {
            'ip': ip,
            'state': state,
            'open_ports': [],
            'services': [],
            'versions': []
        }

        if state == 'up' and 'tcp' in nm[ip]:
            for port in nm[ip]['tcp']:
                port_info = {
                    'port': port,
                    'state': nm[ip]['tcp'][port]['state'],
                    'service': nm[ip]['tcp'][port]['name'],
                    'version': nm[ip]['tcp'][port]['version'],
                }
                result['open_ports'].append(port_info)
                result['services'].append(nm[ip]['tcp'][port]['name'])
                result['versions'].append(nm[ip]['tcp'][port]['version'])

        output_content += f"IP: {result['ip']}\n"
        output_content += f"State: {result['state']}\n"

        if result['open_ports']:
            output_content += "Open Ports: "
            for port_info in result['open_ports']:
                output_content += f"{port_info['port']}, "
            output_content = output_content[:-2] + "\n"

            output_content += "Services: "
            for service in result['services']:
                output_content += f"{service}, "
            output_content = output_content[:-2] + "\n"

            output_content += "Versions: "
            for version in result['versions']:
                output_content += f"{version}, "
            output_content = output_content[:-2] + "\n"
        else:
            output_content += "Open Ports: \n"
            output_content += "Services: \n"
            output_content += "Versions: \n"

        output_content += "\n"

    output_path = config['NETWORK_SCAN']['SCAN_RESULT_PATH']
    with open(output_path, 'w') as file:
        file.write(output_content)

    print(f"Network Scan result was saved to : {output_path}")
