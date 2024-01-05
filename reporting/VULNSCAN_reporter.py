import yaml

def generate_html_report():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    vulnscan_file_path = config['VULNERABILITY_SCANNING']['NUCLEI_OUTPUT_FOLDER_PATH']
    vulnscan_html_temp_path = config['REPORT']['VULNSCAN_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']

    with open(vulnscan_html_temp_path) as f:
        html_template = f.read()

    html_template += f"""
<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <div id="logo_text">
          <!-- class="logo_colour", allows you to change the colour of the text -->
          <h1><a href={info_html_report_path}><b>WEB ARMOR</b></a></h1>
        </div>
      </div>
      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href={info_html_report_path}>Home</a></li>
          <li class="selected"><a href={vulnscan_html_report_path}>Vulnerability SCAN</a></li>
          <li><a href={network_html_report_path}>Network Scan</a></li>
          <li><a href={owasp_html_report_path}>OWASP SCAN</a></li>
          <li><a href={urls_html_report_path}>Crawled Urls</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
        <!-- insert your sidebar items here -->
      </div>
      <div id="content">
        <h1><b>VULNERABILITY SCAN REPORT</b></h1>
    """

    with open(vulnscan_file_path, 'r') as file:
        log_data = file.read()

    entries = log_data.strip().split('\n')

    if len(entries) < 2:
        html_template += """
        <h3>No Vulnerabilities were found</h3>"""
    else:
        html_template += """
    <table>
        <tr>
            <th>Issue</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Details</th>
        </tr>
"""

        for entry in entries:
            parts = entry.split(' ')
            issue = parts[2][1:-1]
            details = ' '.join(parts[5:])
            type_value = parts[3][1:-1] if len(parts) > 3 else ""
            severity = parts[4][1:-1] if len(parts) > 3 else ""
            html_template += f"""   <tr><td>{issue}</td><td>{type_value}</td><td>{severity}</td><td>{details}</td></tr>\n"""
        html_template += """</table>"""

    html_template += """
      </div>
      <div id="content">
      </div>
    </div>
  </div>
</body>

</html>
"""

    with open(vulnscan_html_report_path, 'w') as file:
        file.write(html_template)
          
