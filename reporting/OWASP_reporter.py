import yaml

with open('/root/WebArmor/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    xss_file_path = config['OWASP']['XSS_OUTPUT_PATH']
    open_redir_file_path = config['OWASP']['OP_OUTPUT_PATH']
    owasp_html_temp_path = config['REPORT']['OWASP_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']

def xss_reporter():
    with open(xss_file_path, 'r') as input_file:
        content = [line.split() for line in input_file.readlines()]

    global html_template
    with open(owasp_html_temp_path, 'r') as f:
        html_template = f.read()
    html_template += """
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
              <li><a href={network_html_report_path}>NETWORK SCAN</a></li>
              <li class="selected"><a href={owasp_html_report_path}>OWASP SCAN</a></li>
              <li><a href={urls_html_report_path}>CRAWLED URLS</a></li>
            </ul>
          </div>
        </div>
        <div id="site_content">
          <div class="sidebar">
          <!-- insert your sidebar items here -->
          </div>
          <div id="content">
            <h1><b>XSS Report/POCS</b></h1>
    """

    if len(content) != 0:
        for con in content:
            if len(con) != 0:
                for i in con:
                    if con.index(i) % 2 == 0 and con.index(i) < len(con) - 1:
                        title = i
                        content_text = con[con.index(i) + 1]
                        html_template += f"""
                        <h4><b>{title}</b></h4>
                        <textarea class="textbox" rows="4" cols="50" readonly>{content_text}</textarea>
                        """
    else:
        html_template += """
                <h2><b>No Xss Vulns were found</b></h2>
                """
        

    html_template += """
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """

def open_redir_reporter():
    global html_template
    with open(open_redir_file_path, 'r') as f:
        vuln_urls = [i.split()[1][1:-1] for i in f.readlines()]

    data = []

    def url_parser(url):
        endpoint = url[:url.index('?')]
        payload = url[url.index('=') + 1:]
        parameter = url[url.index('?'):url.index('=')]
        data.append([endpoint, payload, parameter, url])

    for url in vuln_urls:
        url_parser(url)

    html_template += '''
      <h2><b>Open-Redirect Result/POC</b></h2>
      <table>
        <tr>
          <th>Endpoint</th>
          <th>Payload</th>
          <th>Vulnerable Param</th>
          <th>POC</th>
        </tr>
    '''

    for entry in data:
        html_template += f'''
        <tr>
          <td>{entry[0]}</td>
          <td>{entry[1]}</td>
          <td>{entry[2]}</td>
          <td>{entry[3]}</td>
        </tr>
        '''

    html_template += '''</table>
    </div>
      </div>
      <div id="content">
    </div>
    </div>
  </div>
</body>

</html>
    '''

def generate_html_report():
    xss_reporter()
    open_redir_reporter()
    with open(owasp_html_report_path, 'w') as f:
        f.write(html_template)
    print(f'Report saved to : {owasp_html_report_path}')
