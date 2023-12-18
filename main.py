#testing reporting scripts
from reporting import owasp_reporter,INFOReporter,Network_Scan_reporter

owasp_reporter.generate_owasp_report('root/WebArmor/DATA_FOLDER/owasp_scanning/xss.txt','root/WebArmor/DATA_FOLDER/owasp_scanning/open_redirect.txt','root/WebArmor/reporting/utils/owasp.html')
INFOReporter.generate_info_report('root/WebArmor/DATA_FOLDER/asset_discovery/technologies.txt','root/WebArmor/Report.html')
Network_Scan_reporter.generate_network_report('root/WebArmor/DATA_FOLDER/network_scanning/network_scan.txt','root/WebArmor/reporting/utils/network.html')
