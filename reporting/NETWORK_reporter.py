import yaml

def generate_html_report():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    network_file_path = config['NETWORK_SCAN']['SCAN_RESULT_PATH']
    network_html_temp_path = config['REPORT']['NETWORK_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']

    with open(network_file_path, 'r') as file:
        lines = file.readlines()

    data = []
    current_entry = {}

    for line in lines:
        line = line.strip()
        if line:
            key,value = line.split(':')
            print(key)
            current_entry[key.strip()] = value.strip()
        else:
            data.append(current_entry)
            current_entry = {}

    if current_entry:
        data.append(current_entry)

    with open(network_html_temp_path, 'r') as f:
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
          <li><a href={info_html_report_path}>INFO</a></li>
          <li><a href={vulnscan_html_report_path}>VULNERABILITY SCAN</a></li>
          <li class="selected"><a href={network_html_report_path}>NETWORK SCAN</a></li>
          <li><a href={owasp_html_report_path}>OWASP SCAN</a></li>
          <li><a href={urls_html_report_path}>CRAWLED URLS</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
        <!-- insert your sidebar items here -->
      </div>
      <div id="content">
        <h1><b>Network Scan Report</b></h1>
        <table>
          <thead>
            <tr>
              <th>IP</th>
              <th>State</th>
              <th>Open Ports</th>
              <th>Services</th>
              <th>Versions</th>
            </tr>
          </thead>
          <tbody>"""

    for entry in data:
        html_template += f"""<tr>
              <td>{ entry['IP'] }</td>
              <td>{ entry['State'] }</td>
              <td>{ entry['Open Ports'] }</td>
              <td>{ entry['Services'] }</td>
              <td>{ entry['Versions'] }</td>
          </tr>"""

    html_template += """
        </tbody>
      </table>
    </div>
  </div>
</div>
</body>

</html>
"""

    with open(network_html_report_path, 'w') as output_file:
        output_file.write(html_template)
